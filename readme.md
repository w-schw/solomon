# solomon
Compile data from call of duty warzone using opencv and tensorflow

(Work in progress)

Takes screenshots of heads up display data (weapons, ammunition, etc), uses CNN to classify, and records results on a second-by-second basis in a spreadsheet for later analysis.

Weapons classifier is trained on 60k images in 50 classes collected during gameplay. The saved .h5 unfortunately is too large to upload here.

Screenshot locations were set according to a 27inch 2k monitor and haven't been tested with any other configurations.
