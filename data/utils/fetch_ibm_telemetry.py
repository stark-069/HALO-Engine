from qiskit_ibm_runtime import QiskitRuntimeService

def find_my_lgt_jobs():
    service = QiskitRuntimeService()
    print("Fetching last 50 jobs from IBM Quantum Account...\n")
    jobs = service.jobs(limit=50)
    
    for job in jobs:
        # Safely get the backend name
        try:
            backend_name = job.backend().name if job.backend() else "Unknown"
        except Exception:
            backend_name = "Unknown"
            
        job_id = job.job_id()
        
        # FIX: Use creation_date property for V2 jobs
        try:
            created = job.creation_date.strftime("%Y-%m-%d %H:%M:%S")
        except AttributeError:
            created = "Unknown Time"
            
        status = job.status()
        
        # Filter for your target QPUs
        if any(target in backend_name for target in ['marrakesh', 'fez', 'brisbane', 'kyiv']):
            print(f"[FOUND JOB] Backend: {backend_name} | Job ID: {job_id} | Created: {created} | Status: {status}")
            
            # Retrieve backend properties for that specific run if available
            try:
                backend = service.backend(backend_name)
                props = backend.properties()
                t1_vals = [props.t1(q) * 1e6 for q in range(10)] # in microseconds
                t2_vals = [props.t2(q) * 1e6 for q in range(10)]
                print(f"   -> Avg T1 (first 10q): {sum(t1_vals)/len(t1_vals):.2f} us")
                print(f"   -> Avg T2 (first 10q): {sum(t2_vals)/len(t2_vals):.2f} us")
            except Exception as e:
                print(f"   -> Could not fetch exact property snapshot: {e}")
            print("-" * 75)

if __name__ == "__main__":
    find_my_lgt_jobs()