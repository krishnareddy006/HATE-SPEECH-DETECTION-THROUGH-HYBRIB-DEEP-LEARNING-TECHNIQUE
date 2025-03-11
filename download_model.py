import gdown

# Google Drive file ID (must be a string)
file_id = "1i1QIeyMIYIMHYQMHfez2qlZ_knomX-gY"  # Use quotes here
url = f"https://drive.google.com/uc?id={file_id}"
output = "model/ConvolutionalLongShortTermMemory_model.h5"

print("Downloading model from Google Drive...")
gdown.download(url, output, quiet=False)
print("Download complete!")
