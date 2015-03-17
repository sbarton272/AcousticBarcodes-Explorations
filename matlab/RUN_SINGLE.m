%% Run basic algorithm on single file

clear all
close all

%% Load
[audioFiles, Fs] = loadAudio();

%% Extract single test file
audio2 = audioFiles{2}.audio;
audio1 = sum(audio2, 2);
audioFiles{2}.name

%% Plot
plotAudio(audio2, Fs);

%% Pre-Filter noise
fltY = preFilter(audio1, true);
plotAudio(fltY, Fs);

%% Transients
trans = transients(fltY,Fs);
locs = trans/Fs
num = length(locs)

%% Plot found locations
plotTransientLocs(trans, audio1, Fs);

%% Decode
decoded = decodeBarcode(trans, true)
