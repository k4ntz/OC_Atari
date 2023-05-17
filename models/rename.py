import os

for root, dirs, files in os.walk('.'):
    for filename in files:
        if filename == "model_50000000.gz":
            os.rename(os.path.join(root, filename), os.path.join(root, "c51.gz"))

