import os
import time
from multiprocessing import Pool, cpu_count
from typing import List, Dict, Any, Callable

def _parallel_worker_task(args):
    inp_path, out_path, preset_id, export_format, title_case, bullet_clean, trailing_clean, cover, zip_bundle, generate_diff = args
    try:
        from main import process_single_file
        process_single_file(
            inp_path, 
            out_path, 
            preset_id=preset_id, 
            export_format=export_format, 
            title_case=title_case, 
            bullet_clean=bullet_clean, 
            trailing_clean=trailing_clean, 
            inspect=False, 
            cover=cover, 
            zip_bundle=zip_bundle, 
            generate_diff=generate_diff
        )
        return {"file": os.path.basename(inp_path), "status": "Success", "error": None}
    except Exception as e:
        return {"file": os.path.basename(inp_path), "status": "Error", "error": str(e)}

class ParallelBatchEngine:
    @staticmethod
    def process_batch_parallel(input_dir: str, output_dir: str, preset_id: str = "classic_book", export_format: str = "docx", title_case: bool = False, bullet_clean: bool = False, trailing_clean: bool = False, cover: bool = False, zip_bundle: bool = False, generate_diff: bool = False) -> List[Dict[str, Any]]:
        os.makedirs(output_dir, exist_ok=True)
        docx_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.docx') and not f.startswith('~$')]
        
        if not docx_files:
            print("[*] No .docx files found in input directory.")
            return []

        tasks = []
        for fname in docx_files:
            inp = os.path.join(input_dir, fname)
            out = os.path.join(output_dir, f"formatted_{fname}")
            tasks.append((inp, out, preset_id, export_format, title_case, bullet_clean, trailing_clean, cover, zip_bundle, generate_diff))

        cores = min(cpu_count(), len(docx_files))
        print(f"⚡ Starting Parallel Multiprocessing Batch across {cores} CPU Cores for {len(docx_files)} files...")
        
        start_t = time.time()
        with Pool(processes=cores) as pool:
            results = pool.map(_parallel_worker_task, tasks)

        elapsed = time.time() - start_t
        print(f"🎉 Parallel Batch Complete! Processed {len(docx_files)} documents in {elapsed:.2f}s ({len(docx_files)/elapsed:.1f} doc/sec).")
        return results
