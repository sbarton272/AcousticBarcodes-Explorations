%% Run basic algorithm on single file

function RUN_SINGLE(fileName)

close all

%% Load
% [audioFiles, Fs] = loadAudio();

%% Extract single test file
% audio2 = audioFiles{n}.audio; % 1, 3, 5, 8, 9
% audio1 = sum(audio2, 2);
% audioFiles{n}.name

[audio1, Fs] = audioread(fileName)

%% Plot
plotAudio(audio1, Fs);

%% Pre-Filter noise
fltY = preFilter(audio1, true);
plotAudio(fltY, Fs);

%% Transients
trans = transients(fltY, Fs, true);
locs = trans/Fs
num = length(locs)

%% Plot found locations
plotTransientLocs(trans, fltY, Fs);

%% Decode
decoded = decodeBarcode(trans, true)

end
