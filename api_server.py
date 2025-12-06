from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from pathlib import Path
from typing import Optional
import uvicorn
from docling_server import DoclingServer
from datetime import datetime
import shutil

app = FastAPI(
    title="Docling Server API",
    description="API for batch processing PDF documents to extract tables, images, and markdown",
    version="1.0.0"
)

# Configuration
INPUT_DIR = Path("/app/input")
OUTPUT_DIR = Path("/app/output")


class ProcessRequest(BaseModel):
    input_folder: Optional[str] = None
    output_folder: Optional[str] = None


class ProcessResponse(BaseModel):
    status: str
    message: str
    output_folder: str
    timestamp: str


@app.get("/")
def read_root():
    """Root endpoint with API information."""
    return {
        "name": "Docling Server API",
        "version": "1.0.0",
        "description": "Batch process PDF documents to extract tables, images, and markdown",
        "endpoints": {
            "GET /": "API information",
            "GET /health": "Health check",
            "POST /process": "Process all PDFs in input folder",
            "GET /output/{file_path}": "Download output files",
            "GET /summary": "Get processing summary"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint for container orchestration."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "input_folder_exists": INPUT_DIR.exists(),
        "output_folder_exists": OUTPUT_DIR.exists()
    }


@app.post("/process", response_model=ProcessResponse)
async def process_documents(background_tasks: BackgroundTasks):
    """
    Process all PDF files in the input folder.
    Extraction happens in the background.
    """
    try:
        # Check if input folder exists
        if not INPUT_DIR.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Input folder not found: {INPUT_DIR}"
            )

        # Check if there are any PDF files
        pdf_files = list(INPUT_DIR.glob("*.pdf"))
        if not pdf_files:
            raise HTTPException(
                status_code=404,
                detail="No PDF files found in input folder"
            )

        # Create unique output folder for this run
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_output_dir = OUTPUT_DIR / f"run_{timestamp}"
        run_output_dir.mkdir(parents=True, exist_ok=True)

        # Process documents
        server = DoclingServer(str(INPUT_DIR), str(run_output_dir))
        server.process_all_files()

        return ProcessResponse(
            status="success",
            message=f"Processed {len(pdf_files)} PDF file(s)",
            output_folder=str(run_output_dir),
            timestamp=timestamp
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/summary")
def get_summary():
    """Get the latest processing summary."""
    try:
        # Find the most recent run folder
        run_folders = sorted(OUTPUT_DIR.glob("run_*"), reverse=True)

        if not run_folders:
            raise HTTPException(
                status_code=404,
                detail="No processing runs found"
            )

        latest_run = run_folders[0]
        summary_file = latest_run / "summary_report.txt"

        if not summary_file.exists():
            raise HTTPException(
                status_code=404,
                detail="Summary report not found"
            )

        with open(summary_file, 'r', encoding='utf-8') as f:
            summary_content = f.read()

        return {
            "run_folder": latest_run.name,
            "summary": summary_content
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/runs")
def list_runs():
    """List all processing runs."""
    try:
        run_folders = sorted(OUTPUT_DIR.glob("run_*"), reverse=True)

        runs = []
        for run_folder in run_folders:
            summary_file = run_folder / "summary_report.txt"
            runs.append({
                "name": run_folder.name,
                "path": str(run_folder),
                "has_summary": summary_file.exists(),
                "timestamp": run_folder.name.replace("run_", "")
            })

        return {
            "total_runs": len(runs),
            "runs": runs
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/runs/{run_name}")
def delete_run(run_name: str):
    """Delete a specific processing run."""
    try:
        run_folder = OUTPUT_DIR / run_name

        if not run_folder.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Run folder not found: {run_name}"
            )

        if not run_name.startswith("run_"):
            raise HTTPException(
                status_code=400,
                detail="Invalid run folder name"
            )

        shutil.rmtree(run_folder)

        return {
            "status": "success",
            "message": f"Deleted run: {run_name}"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    # Create necessary directories
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Run the API server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
