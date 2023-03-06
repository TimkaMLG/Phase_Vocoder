# Phase Vocoder
Implementation of [algorythm](https://www.guitarpitchshifter.com/algorithm.html) for changing the signal duration without changing the pitch.

# Install
1) Download the repository.
2) Go to the code directory.
3) Install the required packages from [requirements.txt](https://github.com/TimkaMLG/Phase_Vocoder/blob/main/code/requirements.txt). This can be done by: 

`$ pip install -r requirements.txt`

4) Run by bash script [run.sh](https://github.com/TimkaMLG/Phase_Vocoder/blob/main/code/run.sh), you should provide path to input wav file, path to output wav file and scaling factor. Scaling factor should be > 0 and < 1 for compressing audio duration or > 1 for adjusting audio duration.

`$ run.sh <input_path.wav> <output_path.wav> <scaling_factor>`

# Pay attention
Due to calculation errors, the resulting audio is quite noisy, so when playing the result, lower the volume to a minimum to avoid injury to hearing.
