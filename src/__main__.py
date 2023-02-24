"""
This file will be run when the src module gets executed.
@Created by its-haze
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        app="src.api.main:app",
        reload=True,
        log_level="info",
    )  # type: ignore
