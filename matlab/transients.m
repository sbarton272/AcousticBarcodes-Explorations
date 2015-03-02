%% Step 1: Transient isolation
function transients()

close all
clear all

FILE_START = '../audio/black011001-';
FILE_END = '.wav';
FILE_NUMS = 1:9;
for fileNum = FILE_NUMS
    fileName = [FILE_START, num2str(fileNum), FILE_END];
    plotAudio(fileName);
end

%% Basic filtering

%% Transients

end

function plotAudio(file)
%% Load
[y2, Fs] = audioread(file);

% Make single channel
y1 = sum(y2,2);

%% Viz

sound(y1,Fs);

w = linspace(-1/Fs,1/(2*Fs),length(y1));
t = linspace(0,length(y1)/Fs,length(y1));

figure;
subplot(2,1,1); plot(w,fftshift(abs(fft(y1))));
subplot(2,1,2); plot(t,y1);

end