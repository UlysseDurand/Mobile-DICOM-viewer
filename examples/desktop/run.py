import multiprocessing

from mobile_medical_patient_review.app.main import main

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main(exec_mode="desktop")
