from pathlib import Path

from mobile_medical_patient_review import __version__

# Compute local path to serve
serve_path = str(Path(__file__).with_name("serve").resolve())
serve_directory = f"__mobile_medical_patient_review_{__version__}"

# Serve directory for JS/CSS files
serve = {serve_directory: serve_path}

# List of JS files to load (usually from the serve path above)
scripts = [f"{serve_directory}/mobile_medical_patient_review.umd.js"]

# List of CSS files to load (usually from the serve path above)
if (Path(serve_path) / "style.css").exists():
    styles = [serve_directory + "/style.css"]

# List of Vue plugins to install/load
vue_use = ["mobile_medical_patient_review"]

# Uncomment to add entries to the shared state
# state = {}


# Optional if you want to execute custom initialization at module load
def setup(app, **kwargs):
    """Method called at initialization with possibly some custom keyword arguments"""
