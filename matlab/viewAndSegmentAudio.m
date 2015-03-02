%% Loading and examining basic audio file
% NOTE - did not complete this function, just did it in Audacity

clear all
close all

FILENAME = '../audio/011001 2015-02-18 14-01-39.wav';

%% Load audio

[y, Fs] = audioread(FILENAME);

yOne = sum(y,2);

%% Play

sound(y, Fs);

%% View audio freq

window = ceil(.01*Fs);

figure; spectrogram(yOne, window, 'yaxis');

%% View audio mag

time = (0:length(y)-1) / Fs;
figure; plot(time, yOne);

%% Segment

THRESH = .001;
WIN_THRESH = 50;
WINDOW_SIZE = .5 * Fs; % 1 sec

power = yOne.^2;
samplesMask = power > THRESH;
window = ones(WINDOW_SIZE, 1);
samples = cconv(samplesMask, window, length(samplesMask));
segments = samples > WIN_THRESH;

figure; plot(time, -power, time, [diff(segments); 0]);

% Find start and end of segments
indx = find(diff(segments));






