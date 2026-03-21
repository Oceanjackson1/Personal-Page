---
title: "Pydicom"
description: "Python library for working with DICOM (Digital Imaging and Communications in Medicine) files. Use this skill when reading, writing, or modifying medical imaging data in DICOM format, extracting pixel data from medical images (CT, MRI, X-ray, ultra..."
category: "research"
source: "community"
author: "Community"
tags: ["pydicom"]
date: 2026-03-20
---

# Pydicom

## Overview

Pydicom is a pure Python package for working with DICOM files, the standard format for medical imaging data. This skill provides guidance on reading, writing, and manipulating DICOM files, including working with pixel data, metadata, and various compression formats.

## When to Use This Skill

Use this skill when working with:
- Medical imaging files (CT, MRI, X-ray, ultrasound, PET, etc.)
- DICOM datasets requiring metadata extraction or modification
- Pixel data extraction and image processing from medical scans
- DICOM anonymization for research or data sharing
- Converting DICOM files to standard image formats
- Compressed DICOM data requiring decompression
- DICOM sequences and structured reports
- Multi-slice volume reconstruction
- PACS (Picture Archiving and Communication System) integration

## Installation

Install pydicom and common dependencies:

```bash
uv pip install pydicom
uv pip install pillow  # For image format conversion
uv pip install numpy   # For pixel array manipulation
uv pip install matplotlib  # For visualization
```

For handling compressed DICOM files, additional packages may be needed:

```bash
uv pip install pylibjpeg pylibjpeg-libjpeg pylibjpeg-openjpeg  # JPEG compression
uv pip install python-gdcm  # Alternative compression handler
```

## Core Workflows

### Reading DICOM Files

Read a DICOM file using `pydicom.dcmread()`:

```python
import pydicom

# Read a DICOM file
ds = pydicom.dcmread('path/to/file.dcm')

# Access metadata
print(f"Patient Name: {ds.PatientName}")
print(f"Study Date: {ds.StudyDate}")
print(f"Modality: {ds.Modality}")

# Display all elements
print(ds)
```

**Key points:**
- `dcmread()` returns a `Dataset` object
- Access data elements using attribute notation (e.g., `ds.PatientName`) or tag notation (e.g., `ds[0x0010, 0x0010]`)
- Use `ds.file_meta` to access file metadata like Transfer Syntax UID
- Handle missing attributes with `getattr(ds, 'AttributeName', default_value)` or `hasattr(ds, 'AttributeName')`

### Working with Pixel Data

Extract and manipulate image data from DICOM files:

```python
import pydicom
import numpy as np
import matplotlib.pyplot as plt

# Read DICOM file
ds = pydicom.dcmread('image.dcm')

# Get pixel array (requires numpy)
pixel_array = ds.pixel_array

# Image information
print(f"Shape: {pixel_array.shape}")
print(f"Data type: {pixel_array.dtype}")
print(f"Rows: {ds.Rows}, Columns: {ds.Columns}")

# Apply windowing for display (CT/MRI)
if hasattr(ds, 'WindowCenter') and hasattr(ds, 'WindowWidth'):
    from pydicom.pixel_data_handlers.util import apply_voi_lut
    windowed_image = apply_voi_lut(pixel_array, ds)
else:
    windowed_image = pixel_array

# Display image
plt.imshow(windowed_image, cmap='gray')
plt.title(f"{ds.Modality} - {ds.StudyDescription}")
plt.axis('off')
plt.show()
```

**Working with color images:**

```python
# RGB images have shape (rows, columns, 3)
if ds.PhotometricInterpretation == 'RGB':
    rgb_image = ds.pixel_array
    plt.imshow(rgb_image)
elif ds.PhotometricInterpretation == 'YBR_FULL':
    from pydicom.pixel_data_handlers.util import convert_color_space
    rgb_image = convert_color_space(ds.pixel_array, 'YBR_FULL', 'RGB')
    plt.imshow(rgb_image)
```

**Multi-frame images (videos/series):**

```python
# For multi-frame DICOM files
if hasattr(ds, 'NumberOfFrames') and ds.NumberOfFrames > 1:
    frames = ds.pixel_array  # Shape: (num_frames, rows, columns)
    print(f"Number of frames: {frames.shape[0]}")

    # Display specific frame
    plt.imshow(frames[0], cmap='gray')
```

### Converting DICOM to Image Formats

Use the provided `dicom_to_image.py` script or convert manually:

```python
from PIL import Image
import pydicom
import numpy as np

ds = pydicom.dcmread('input.dcm')
pixel_array = ds.pixel_array

# Normalize to 0-255 range
if pixel_array.dtype != np.uint8:
    pixel_array = ((pixel_array - pixel_array.min()) /
                   (pixel_array.max() - pixel_array.min()) * 255).astype(np.uint8)

# Save as PNG
image = Image.fromarray(pixel_array)
image.save('output.png')
```

Use the script: `python scripts/dicom_to_image.py input.dcm output.png`

### Modifying Metadata

Modify DICOM data elements:

```python
import pydicom
from datetime import datetime

ds = pydicom.dcmread('input.dcm')

# Modify existing elements
ds.PatientName = "Doe^John"
ds.StudyDate = datetime.now().strftime('%Y%m%d')
ds.StudyDescription = "Modified Study"

# Add new elements
ds.SeriesNumber = 1
ds.SeriesDescription = "New Series"

# Remove elements
if hasattr(ds, 'PatientComments'):
    delattr(ds, 'PatientComments')
# Or using del
if 'PatientComments' in ds:
    del ds.PatientComments

# Save modified file
ds.save_as('modified.dcm')
```

### Anonymizing DICOM Files

Remove or replace patient identifiable information:

```python
import pydicom
from datetime import datetime

ds = pydicom.dcmread('input.dcm')

# Tags commonly containing PHI (Protected Health Information)
tags_to_anonymize = [
    'PatientName', 'PatientID', 'PatientBirthDate',
    'PatientSex', 'PatientAge', 'PatientAddress',
    'InstitutionName', 'InstitutionAddress',
    'ReferringPhysicianName', 'PerformingPhysicianName',
    'OperatorsName', 'StudyDescription', 'SeriesDescription',
]

# Remove or replace sensitive data
for tag in tags_to_anonymize:
    if hasattr(ds, tag):
        if tag in ['PatientName', 'PatientID']:
            setattr(ds, tag, 'ANONYMOUS')
        elif tag == 'PatientBirthDate':
            setattr(ds, tag, '19000101')
        else:
            delattr(ds, tag)

# Update dates to maintain temporal relationships
if hasattr(ds, 'StudyDate'):
    # Shift dates by a random offset
    ds.StudyDate = '20000101'

# Keep pixel data intact
ds.save_as('anonymized.dcm')
```

Use the provided script: `python scripts/anonymize_dicom.py input.dcm output.dcm`

### Writing DICOM Files

Create DICOM files from scratch:

```python
import pydicom
from pydicom.dataset import Dataset, FileDataset
from datetime import datetime
import numpy as np

# Create file meta information
file_meta = Dataset()
file_meta.MediaStorageSOPClassUID = pydicom.uid.generate_uid()
file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian

# Create the FileDataset instance
ds = FileDataset('new_dicom.dcm', {}, file_meta=file_meta, preamble=b"\0" * 128)

# Add required DICOM elements
ds.PatientName = "Test^Patient"
ds.PatientID = "123456"
ds.Modality = "CT"
ds.StudyDate = datetime.now().strftime('%Y%m%d')
ds.StudyTime = datetime.now().strftime('%H%M%S')
ds.ContentDate = ds.StudyDate
ds.ContentTime = ds.StudyTime

# Add image-specific elements
ds.SamplesPerPixel = 1
ds.PhotometricInterpretation = "MONOCHROME2"
ds.Rows = 512
ds.Columns = 512
ds.BitsAllocated = 16
ds.BitsStored = 16
ds.HighBit = 15
ds.PixelRepresentation = 0

# Create pixel data
pixel_array = np.random.randint(0, 4096, (512, 512), dtype=np.uint16)
ds.PixelData = pixel_array.tobytes()

# Add required UIDs
ds.SOPClassUID = pydicom.uid.CTImageStorage
ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
ds.SeriesInstanceUID = pydicom.uid.generate_uid()
ds.StudyInstanceUID = pydicom.uid.generate_uid()

# Save the file
ds.save_as('new_dicom.dcm')
```

### Compression and Decompression

Handle compressed DICOM files:

```python
import pydicom

# Read compressed DICOM file
ds = pydicom.dcmread('compressed.dcm')

# Check transfer syntax
print(f"Transfer Syntax: {ds.file_meta.TransferSyntaxUID}")
print(f"Transfer Syntax Name: {ds.file_meta.TransferSyntaxUID.name}")

# Decompress and save as uncompressed
ds.decompress()
ds.save_as('uncompressed.dcm', write_like_original=False)

# Or compress when saving (requires appropriate encoder)
ds_uncompressed = pydicom.dcmread('uncompressed.dcm')
ds_uncompressed.compress(pydicom.uid.JPEGBaseline8Bit)
ds_uncompressed.save_as('compressed_jpeg.dcm')
```

**Common transfer syntaxes:**
- `ExplicitVRLittleEndian` - Uncompressed, most common
- `JPEGBaseline8Bit` - JPEG lossy compression
- `JPEGLossless` - JPEG lossless compression
- `JPEG2000Lossless` - JPEG 2000 lossless
- `RLELossless` - Run-Length Encoding lossless

See `references/transfer_syntaxes.md` for complete list.

### Working with DICOM Sequences

Handle nested data structures:

```python
import pydicom

ds = pydicom.dcmread('file.dcm')

# Access sequences
if 'ReferencedStudySequence' in ds:
    for item in ds.ReferencedStudySequence:
        print(f"Referenced SOP Instance UID: {item.ReferencedSOPInstanceUID}")

# Create a sequence
from pydicom.sequence import Sequence

sequence_item = Dataset()
sequence_item.ReferencedSOPClassUID = pydicom.uid.CTImageStorage
sequence_item.ReferencedSOPInstanceUID = pydicom.uid.generate_uid()

ds.ReferencedImageSequence = Sequence([sequence_item])
```

### Processing DICOM Series

Work with multiple related DICOM files:

```python
import pydicom
import numpy as np
from pathlib import Path

# Read all DICOM files in a directory
dicom_dir = Path('dicom_series/')
slices = []

for file_path in dicom_dir.glob('*.dcm'):
    ds = pydicom.dcmread(file_path)
    slices.append(ds)

# Sort by slice location or instance number
slices.sort(key=lambda x: float(x.ImagePositionPatient[2]))
# Or: slices.sort(key=lambda x: int(x.InstanceNumber))

# Create 3D volume
volume = np.stack([s.pixel_array for s in slices])
print(f"Volume shape: {volume.shape}")  # (num_slices, rows, columns)

# Get spacing information for proper scaling
pixel_spacing = slices[0].PixelSpacing  # [row_spacing, col_spacing]
slice_thickness = slices[0].SliceThickness
print(f"Voxel size: {pixel_spacing[0]}x{pixel_spacing[1]}x{slice_thickness} mm")
```

## Helper Scripts

This skill includes utility scripts in the `scripts/` directory:

### anonymize_dicom.py
Anonymize DICOM files by removing or replacing Protected Health Information (PHI).

```bash
python scripts/anonymize_dicom.py input.dcm output.dcm
```

### dicom_to_image.py
Convert DICOM files to common image formats (PNG, JPEG, TIFF).

```bash
python scripts/dicom_to_image.py input.dcm output.png
python scripts/dicom_to_image.py input.dcm output.jpg --format JPEG
```

### extract_metadata.py
Extract and display DICOM metadata in a readable format.

```bash
python scripts/extract_metadata.py file.dcm
python scripts/extract_metadata.py file.dcm --output metadata.txt
```

## Reference Materials

Detailed reference information is available in the `references/` directory:

- **common_tags.md**: Comprehensive list of commonly used DICOM tags organized by category (Patient, Study, Series, Image, etc.)
- **transfer_syntaxes.md**: Complete reference of DICOM transfer syntaxes and compression formats

## Common Issues and Solutions

**Issue: "Unable to decode pixel data"**
- Solution: Install additional compression handlers: `uv pip install pylibjpeg pylibjpeg-libjpeg python-gdcm`

**Issue: "AttributeError" when accessing tags**
- Solution: Check if attribute exists with `hasattr(ds, 'AttributeName')` or use `ds.get('AttributeName', default)`

**Issue: Incorrect image display (too dark/bright)**
- Solution: Apply VOI LUT windowing: `apply_voi_lut(pixel_array, ds)` or manually adjust with `WindowCenter` and `WindowWidth`

**Issue: Memory issues with large series**
- Solution: Process files iteratively, use memory-mapped arrays, or downsample images

## Best Practices

1. **Always check for required attributes** before accessing them using `hasattr()` or `get()`
2. **Preserve file metadata** when modifying files by using `save_as()` with `write_like_original=True`
3. **Use Transfer Syntax UIDs** to understand compression format before processing pixel data
4. **Handle exceptions** when reading files from untrusted sources
5. **Apply proper windowing** (VOI LUT) for medical image visualization
6. **Maintain spatial information** (pixel spacing, slice thickness) when processing 3D volumes
7. **Verify anonymization** thoroughly before sharing medical data
8. **Use UIDs correctly** - generate new UIDs when creating new instances, preserve them when modifying

## Documentation

Official pydicom documentation: https://pydicom.github.io/pydicom/dev/
- User Guide: https://pydicom.github.io/pydicom/dev/guides/user/index.html
- Tutorials: https://pydicom.github.io/pydicom/dev/tutorials/index.html
- API Reference: https://pydicom.github.io/pydicom/dev/reference/index.html
- Examples: https://pydicom.github.io/pydicom/dev/auto_examples/index.html

---

## Reference: Common_Tags

# Common DICOM Tags Reference

This document provides a comprehensive list of commonly used DICOM tags organized by category. Tags can be accessed in pydicom using attribute notation (e.g., `ds.PatientName`) or tag tuple notation (e.g., `ds[0x0010, 0x0010]`).

## Patient Information Tags

| Tag | Name | Type | Description |
|-----|------|------|-------------|
| (0010,0010) | PatientName | PN | Patient's full name |
| (0010,0020) | PatientID | LO | Primary identifier for the patient |
| (0010,0030) | PatientBirthDate | DA | Date of birth (YYYYMMDD) |
| (0010,0032) | PatientBirthTime | TM | Time of birth (HHMMSS) |
| (0010,0040) | PatientSex | CS | Patient's sex (M, F, O) |
| (0010,1010) | PatientAge | AS | Patient's age (format: nnnD/W/M/Y) |
| (0010,1020) | PatientSize | DS | Patient's height in meters |
| (0010,1030) | PatientWeight | DS | Patient's weight in kilograms |
| (0010,1040) | PatientAddress | LO | Patient's mailing address |
| (0010,2160) | EthnicGroup | SH | Ethnic group of patient |
| (0010,4000) | PatientComments | LT | Additional comments about patient |

## Study Information Tags

| Tag | Name | Type | Description |
|-----|------|------|-------------|
| (0020,000D) | StudyInstanceUID | UI | Unique identifier for the study |
| (0008,0020) | StudyDate | DA | Date study started (YYYYMMDD) |
| (0008,0030) | StudyTime | TM | Time study started (HHMMSS) |
| (0008,1030) | StudyDescription | LO | Description of the study |
| (0020,0010) | StudyID | SH | User or site-defined study identifier |
| (0008,0050) | AccessionNumber | SH | RIS-generated study identifier |
| (0008,0090) | ReferringPhysicianName | PN | Name of patient's referring physician |
| (0008,1060) | NameOfPhysiciansReadingStudy | PN | Name of physician(s) reading study |
| (0008,1080) | AdmittingDiagnosesDescription | LO | Diagnosis description at admission |

## Series Information Tags

| Tag | Name | Type | Description |
|-----|------|------|-------------|
| (0020,000E) | SeriesInstanceUID | UI | Unique identifier for the series |
| (0020,0011) | SeriesNumber | IS | Numeric identifier for this series |
| (0008,103E) | SeriesDescription | LO | Description of the series |
| (0008,0060) | Modality | CS | Type of equipment (CT, MR, US, etc.) |
| (0008,0021) | SeriesDate | DA | Date series started (YYYYMMDD) |
| (0008,0031) | SeriesTime | TM | Time series started (HHMMSS) |
| (0018,0015) | BodyPartExamined | CS | Body part examined |
| (0018,5100) | PatientPosition | CS | Patient position (HFS, FFS, etc.) |
| (0020,0060) | Laterality | CS | Laterality of paired body part (R, L) |

## Image Information Tags

| Tag | Name | Type | Description |
|-----|------|------|-------------|
| (0008,0018) | SOPInstanceUID | UI | Unique identifier for this instance |
| (0020,0013) | InstanceNumber | IS | Number that identifies this image |
| (0008,0008) | ImageType | CS | Image identification characteristics |
| (0008,0023) | ContentDate | DA | Date of content creation (YYYYMMDD) |
| (0008,0033) | ContentTime | TM | Time of content creation (HHMMSS) |
| (0020,0032) | ImagePositionPatient | DS | Position of image (x, y, z) in mm |
| (0020,0037) | ImageOrientationPatient | DS | Direction cosines of image rows/columns |
| (0020,1041) | SliceLocation | DS | Relative position of image plane |
| (0018,0050) | SliceThickness | DS | Slice thickness in mm |
| (0018,0088) | SpacingBetweenSlices | DS | Spacing between slices in mm |

## Pixel Data Tags

| Tag | Name | Type | Description |
|-----|------|------|-------------|
| (7FE0,0010) | PixelData | OB/OW | Actual pixel data of the image |
| (0028,0010) | Rows | US | Number of rows in image |
| (0028,0011) | Columns | US | Number of columns in image |
| (0028,0100) | BitsAllocated | US | Bits allocated for each pixel sample |
| (0028,0101) | BitsStored | US | Bits stored for each pixel sample |
| (0028,0102) | HighBit | US | Most significant bit for pixel sample |
| (0028,0103) | PixelRepresentation | US | 0=unsigned, 1=signed |
| (0028,0002) | SamplesPerPixel | US | Number of samples per pixel (1 or 3) |
| (0028,0004) | PhotometricInterpretation | CS | Color space (MONOCHROME2, RGB, etc.) |
| (0028,0006) | PlanarConfiguration | US | Color pixel data arrangement |
| (0028,0030) | PixelSpacing | DS | Physical spacing [row, column] in mm |
| (0028,0008) | NumberOfFrames | IS | Number of frames in multi-frame image |
| (0028,0034) | PixelAspectRatio | IS | Ratio of vertical to horizontal pixel |

## Windowing and Display Tags

| Tag | Name | Type | Description |
|-----|------|------|-------------|
| (0028,1050) | WindowCenter | DS | Window center for display |
| (0028,1051) | WindowWidth | DS | Window width for display |
| (0028,1052) | RescaleIntercept | DS | b in output = m*SV + b |
| (0028,1053) | RescaleSlope | DS | m in output = m*SV + b |
| (0028,1054) | RescaleType | LO | Type of rescaling (HU, etc.) |
| (0028,1055) | WindowCenterWidthExplanation | LO | Explanation of window values |
| (0028,3010) | VOILUTSequence | SQ | VOI LUT description |

## CT-Specific Tags

| Tag | Name | Type | Description |
|-----|------|------|-------------|
| (0018,0060) | KVP | DS | Peak kilovoltage |
| (0018,1030) | ProtocolName | LO | Scan protocol name |
| (0018,1100) | ReconstructionDiameter | DS | Diameter of reconstruction circle |
| (0018,1110) | DistanceSourceToDetector | DS | Distance in mm |
| (0018,1111) | DistanceSourceToPatient | DS | Distance in mm |
| (0018,1120) | GantryDetectorTilt | DS | Gantry tilt in degrees |
| (0018,1130) | TableHeight | DS | Table height in mm |
| (0018,1150) | ExposureTime | IS | Exposure time in ms |
| (0018,1151) | XRayTubeCurrent | IS | X-ray tube current in mA |
| (0018,1152) | Exposure | IS | Exposure in mAs |
| (0018,1160) | FilterType | SH | X-ray filter material |
| (0018,1210) | ConvolutionKernel | SH | Reconstruction algorithm |

## MR-Specific Tags

| Tag | Name | Type | Description |
|-----|------|------|-------------|
| (0018,0080) | RepetitionTime | DS | TR in ms |
| (0018,0081) | EchoTime | DS | TE in ms |
| (0018,0082) | InversionTime | DS | TI in ms |
| (0018,0083) | NumberOfAverages | DS | Number of times data was averaged |
| (0018,0084) | ImagingFrequency | DS | Frequency in MHz |
| (0018,0085) | ImagedNucleus | SH | Nucleus that is imaged (1H, etc.) |
| (0018,0086) | EchoNumbers | IS | Echo number(s) |
| (0018,0087) | MagneticFieldStrength | DS | Field strength in Tesla |
| (0018,0088) | SpacingBetweenSlices | DS | Spacing in mm |
| (0018,0089) | NumberOfPhaseEncodingSteps | IS | Number of encoding steps |
| (0018,0091) | EchoTrainLength | IS | Number of echoes in a train |
| (0018,0093) | PercentSampling | DS | Fraction of acquisition matrix sampled |
| (0018,0094) | PercentPhaseFieldOfView | DS | Ratio of phase to frequency FOV |
| (0018,1030) | ProtocolName | LO | Scan protocol name |
| (0018,1314) | FlipAngle | DS | Flip angle in degrees |

## File Meta Information Tags

| Tag | Name | Type | Description |
|-----|------|------|-------------|
| (0002,0000) | FileMetaInformationGroupLength | UL | Length of file meta information |
| (0002,0001) | FileMetaInformationVersion | OB | Version of file meta information |
| (0002,0002) | MediaStorageSOPClassUID | UI | SOP Class UID |
| (0002,0003) | MediaStorageSOPInstanceUID | UI | SOP Instance UID |
| (0002,0010) | TransferSyntaxUID | UI | Transfer syntax UID |
| (0002,0012) | ImplementationClassUID | UI | Implementation class UID |
| (0002,0013) | ImplementationVersionName | SH | Implementation version name |

## Equipment Tags

| Tag | Name | Type | Description |
|-----|------|------|-------------|
| (0008,0070) | Manufacturer | LO | Equipment manufacturer |
| (0008,0080) | InstitutionName | LO | Institution name |
| (0008,0081) | InstitutionAddress | ST | Institution address |
| (0008,1010) | StationName | SH | Equipment station name |
| (0008,1040) | InstitutionalDepartmentName | LO | Department name |
| (0008,1050) | PerformingPhysicianName | PN | Physician performing procedure |
| (0008,1070) | OperatorsName | PN | Operator name(s) |
| (0008,1090) | ManufacturerModelName | LO | Model name |
| (0018,1000) | DeviceSerialNumber | LO | Device serial number |
| (0018,1020) | SoftwareVersions | LO | Software version(s) |

## Timing Tags

| Tag | Name | Type | Description |
|-----|------|------|-------------|
| (0008,0012) | InstanceCreationDate | DA | Date instance was created |
| (0008,0013) | InstanceCreationTime | TM | Time instance was created |
| (0008,0022) | AcquisitionDate | DA | Date acquisition started |
| (0008,0032) | AcquisitionTime | TM | Time acquisition started |
| (0008,002A) | AcquisitionDateTime | DT | Acquisition date and time |

## DICOM Value Representations (VR)

Common value representation types used in DICOM:

- **AE**: Application Entity (max 16 chars)
- **AS**: Age String (nnnD/W/M/Y)
- **CS**: Code String (max 16 chars)
- **DA**: Date (YYYYMMDD)
- **DS**: Decimal String
- **DT**: Date Time (YYYYMMDDHHMMSS.FFFFFF&ZZXX)
- **IS**: Integer String
- **LO**: Long String (max 64 chars)
- **LT**: Long Text (max 10240 chars)
- **PN**: Person Name
- **SH**: Short String (max 16 chars)
- **SQ**: Sequence of Items
- **ST**: Short Text (max 1024 chars)
- **TM**: Time (HHMMSS.FFFFFF)
- **UI**: Unique Identifier (UID)
- **UL**: Unsigned Long (4 bytes)
- **US**: Unsigned Short (2 bytes)
- **OB**: Other Byte String
- **OW**: Other Word String

## Usage Examples

### Accessing Tags by Name
```python
patient_name = ds.PatientName
study_date = ds.StudyDate
modality = ds.Modality
```

### Accessing Tags by Number
```python
patient_name = ds[0x0010, 0x0010].value
study_date = ds[0x0008, 0x0020].value
modality = ds[0x0008, 0x0060].value
```

### Checking if Tag Exists
```python
if hasattr(ds, 'PatientName'):
    print(ds.PatientName)

# Or using 'in' operator
if (0x0010, 0x0010) in ds:
    print(ds[0x0010, 0x0010].value)
```

### Safe Access with Default Value
```python
patient_name = getattr(ds, 'PatientName', 'Unknown')
study_desc = ds.get('StudyDescription', 'No description')
```

## References

- DICOM Standard: https://www.dicomstandard.org/
- DICOM Tag Browser: https://dicom.innolitics.com/ciods
- Pydicom Documentation: https://pydicom.github.io/pydicom/

---

## Reference: Transfer_Syntaxes

# DICOM Transfer Syntaxes Reference

This document provides a comprehensive reference for DICOM transfer syntaxes and compression formats. Transfer syntaxes define how DICOM data is encoded, including byte ordering, compression method, and other encoding rules.

## Overview

A Transfer Syntax UID specifies:
1. **Byte ordering**: Little Endian or Big Endian
2. **Value Representation (VR)**: Implicit or Explicit
3. **Compression**: None, or specific compression algorithm

## Uncompressed Transfer Syntaxes

### Implicit VR Little Endian (1.2.840.10008.1.2)
- **Default** transfer syntax
- Value Representations are implicit (not explicitly encoded)
- Little Endian byte ordering
- **Pydicom constant**: `pydicom.uid.ImplicitVRLittleEndian`

**Usage:**
```python
import pydicom
ds.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
```

### Explicit VR Little Endian (1.2.840.10008.1.2.1)
- **Most common** transfer syntax
- Value Representations are explicit
- Little Endian byte ordering
- **Pydicom constant**: `pydicom.uid.ExplicitVRLittleEndian`

**Usage:**
```python
ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
```

### Explicit VR Big Endian (1.2.840.10008.1.2.2) - RETIRED
- Value Representations are explicit
- Big Endian byte ordering
- **Deprecated** - not recommended for new implementations
- **Pydicom constant**: `pydicom.uid.ExplicitVRBigEndian`

## JPEG Compression

### JPEG Baseline (Process 1) (1.2.840.10008.1.2.4.50)
- **Lossy** compression
- 8-bit samples only
- Most widely supported JPEG format
- **Pydicom constant**: `pydicom.uid.JPEGBaseline8Bit`

**Dependencies:** Requires `pylibjpeg` or `pillow`

**Usage:**
```python
# Compress
ds.compress(pydicom.uid.JPEGBaseline8Bit)

# Decompress
ds.decompress()
```

### JPEG Extended (Process 2 & 4) (1.2.840.10008.1.2.4.51)
- **Lossy** compression
- 8-bit and 12-bit samples
- **Pydicom constant**: `pydicom.uid.JPEGExtended12Bit`

### JPEG Lossless, Non-Hierarchical (Process 14) (1.2.840.10008.1.2.4.57)
- **Lossless** compression
- First-Order Prediction
- **Pydicom constant**: `pydicom.uid.JPEGLossless`

**Dependencies:** Requires `pylibjpeg-libjpeg` or `gdcm`

### JPEG Lossless, Non-Hierarchical, First-Order Prediction (1.2.840.10008.1.2.4.70)
- **Lossless** compression
- Uses Process 14 Selection Value 1
- **Pydicom constant**: `pydicom.uid.JPEGLosslessSV1`

**Usage:**
```python
# Compress to JPEG Lossless
ds.compress(pydicom.uid.JPEGLossless)
```

### JPEG-LS Lossless (1.2.840.10008.1.2.4.80)
- **Lossless** compression
- Low complexity, good compression
- **Pydicom constant**: `pydicom.uid.JPEGLSLossless`

**Dependencies:** Requires `pylibjpeg-libjpeg` or `gdcm`

### JPEG-LS Lossy (Near-Lossless) (1.2.840.10008.1.2.4.81)
- **Near-lossless** compression
- Allows controlled loss of precision
- **Pydicom constant**: `pydicom.uid.JPEGLSNearLossless`

## JPEG 2000 Compression

### JPEG 2000 Lossless Only (1.2.840.10008.1.2.4.90)
- **Lossless** compression
- Wavelet-based compression
- Better compression than JPEG Lossless
- **Pydicom constant**: `pydicom.uid.JPEG2000Lossless`

**Dependencies:** Requires `pylibjpeg-openjpeg`, `gdcm`, or `pillow`

**Usage:**
```python
# Compress to JPEG 2000 Lossless
ds.compress(pydicom.uid.JPEG2000Lossless)
```

### JPEG 2000 (1.2.840.10008.1.2.4.91)
- **Lossy or lossless** compression
- Wavelet-based compression
- High quality at low bit rates
- **Pydicom constant**: `pydicom.uid.JPEG2000`

**Dependencies:** Requires `pylibjpeg-openjpeg`, `gdcm`, or `pillow`

### JPEG 2000 Part 2 Multi-component Lossless (1.2.840.10008.1.2.4.92)
- **Lossless** compression
- Supports multi-component images
- **Pydicom constant**: `pydicom.uid.JPEG2000MCLossless`

### JPEG 2000 Part 2 Multi-component (1.2.840.10008.1.2.4.93)
- **Lossy or lossless** compression
- Supports multi-component images
- **Pydicom constant**: `pydicom.uid.JPEG2000MC`

## RLE Compression

### RLE Lossless (1.2.840.10008.1.2.5)
- **Lossless** compression
- Run-Length Encoding
- Simple, fast algorithm
- Good for images with repeated values
- **Pydicom constant**: `pydicom.uid.RLELossless`

**Dependencies:** Built into pydicom (no additional packages needed)

**Usage:**
```python
# Compress with RLE
ds.compress(pydicom.uid.RLELossless)

# Decompress
ds.decompress()
```

## Deflated Transfer Syntaxes

### Deflated Explicit VR Little Endian (1.2.840.10008.1.2.1.99)
- Uses ZLIB compression on entire dataset
- Not commonly used
- **Pydicom constant**: `pydicom.uid.DeflatedExplicitVRLittleEndian`

## MPEG Compression

### MPEG2 Main Profile @ Main Level (1.2.840.10008.1.2.4.100)
- **Lossy** video compression
- For multi-frame images/videos
- **Pydicom constant**: `pydicom.uid.MPEG2MPML`

### MPEG2 Main Profile @ High Level (1.2.840.10008.1.2.4.101)
- **Lossy** video compression
- Higher resolution than MPML
- **Pydicom constant**: `pydicom.uid.MPEG2MPHL`

### MPEG-4 AVC/H.264 High Profile (1.2.840.10008.1.2.4.102-106)
- **Lossy** video compression
- Various levels (BD, 2D, 3D, Stereo)
- Modern video codec

## Checking Transfer Syntax

### Identify Current Transfer Syntax
```python
import pydicom

ds = pydicom.dcmread('image.dcm')

# Get transfer syntax UID
ts_uid = ds.file_meta.TransferSyntaxUID
print(f"Transfer Syntax UID: {ts_uid}")

# Get human-readable name
print(f"Transfer Syntax Name: {ts_uid.name}")

# Check if compressed
print(f"Is compressed: {ts_uid.is_compressed}")
```

### Common Checks
```python
# Check if little endian
if ts_uid.is_little_endian:
    print("Little Endian")

# Check if implicit VR
if ts_uid.is_implicit_VR:
    print("Implicit VR")

# Check compression type
if 'JPEG' in ts_uid.name:
    print("JPEG compressed")
elif 'JPEG2000' in ts_uid.name:
    print("JPEG 2000 compressed")
elif 'RLE' in ts_uid.name:
    print("RLE compressed")
```

## Decompression

### Automatic Decompression
Pydicom can automatically decompress pixel data when accessing `pixel_array`:

```python
import pydicom

# Read compressed DICOM
ds = pydicom.dcmread('compressed.dcm')

# Pixel data is automatically decompressed
pixel_array = ds.pixel_array  # Decompresses if needed
```

### Manual Decompression
```python
import pydicom

ds = pydicom.dcmread('compressed.dcm')

# Decompress in-place
ds.decompress()

# Now save as uncompressed
ds.save_as('uncompressed.dcm', write_like_original=False)
```

## Compression

### Compressing DICOM Files
```python
import pydicom

ds = pydicom.dcmread('uncompressed.dcm')

# Compress using JPEG 2000 Lossless
ds.compress(pydicom.uid.JPEG2000Lossless)
ds.save_as('compressed_j2k.dcm')

# Compress using RLE Lossless (no additional dependencies)
ds.compress(pydicom.uid.RLELossless)
ds.save_as('compressed_rle.dcm')

# Compress using JPEG Baseline (lossy)
ds.compress(pydicom.uid.JPEGBaseline8Bit)
ds.save_as('compressed_jpeg.dcm')
```

### Compression with Custom Encoding Parameters
```python
import pydicom
from pydicom.encoders import JPEGLSLosslessEncoder

ds = pydicom.dcmread('uncompressed.dcm')

# Compress with custom parameters
ds.compress(pydicom.uid.JPEGLSLossless, encoding_plugin='pylibjpeg')
```

## Installing Compression Handlers

Different transfer syntaxes require different Python packages:

### JPEG Baseline/Extended
```bash
pip install pylibjpeg pylibjpeg-libjpeg
# Or
pip install pillow
```

### JPEG Lossless/JPEG-LS
```bash
pip install pylibjpeg pylibjpeg-libjpeg
# Or
pip install python-gdcm
```

### JPEG 2000
```bash
pip install pylibjpeg pylibjpeg-openjpeg
# Or
pip install python-gdcm
# Or
pip install pillow
```

### RLE
No additional packages needed - built into pydicom

### Comprehensive Installation
```bash
# Install all common handlers
pip install pylibjpeg pylibjpeg-libjpeg pylibjpeg-openjpeg python-gdcm
```

## Checking Available Handlers

```python
import pydicom

# List available pixel data handlers
from pydicom.pixel_data_handlers.util import get_pixel_data_handlers
handlers = get_pixel_data_handlers()

print("Available handlers:")
for handler in handlers:
    print(f"  - {handler.__name__}")
```

## Best Practices

1. **Use Explicit VR Little Endian** for maximum compatibility when creating new files
2. **Use JPEG 2000 Lossless** for good compression with no quality loss
3. **Use RLE Lossless** if you can't install additional dependencies
4. **Check Transfer Syntax** before processing to ensure you have the right handlers
5. **Test decompression** before deploying to ensure all required packages are installed
6. **Preserve original** transfer syntax when possible using `write_like_original=True`
7. **Consider file size** vs. quality tradeoffs when choosing lossy compression
8. **Use lossless compression** for diagnostic images to maintain clinical quality

## Common Issues

### Issue: "Unable to decode pixel data"
**Cause:** Missing compression handler
**Solution:** Install the appropriate package (see Installing Compression Handlers above)

### Issue: "Unsupported Transfer Syntax"
**Cause:** Rare or unsupported compression format
**Solution:** Try installing `python-gdcm` which supports more formats

### Issue: "Pixel data decompressed but looks wrong"
**Cause:** May need to apply VOI LUT or rescale
**Solution:** Use `apply_voi_lut()` or apply `RescaleSlope`/`RescaleIntercept`

## References

- DICOM Standard Part 5 (Data Structures and Encoding): https://dicom.nema.org/medical/dicom/current/output/chtml/part05/PS3.5.html
- Pydicom Transfer Syntax Documentation: https://pydicom.github.io/pydicom/stable/guides/user/transfer_syntaxes.html
- Pydicom Compression Guide: https://pydicom.github.io/pydicom/stable/old/image_data_compression.html
