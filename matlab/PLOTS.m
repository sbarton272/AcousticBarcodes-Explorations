%% Run plots

clear all
close all

[audio2, Fs] = audioread('../audio/black011001-2.wav');
audio1 = sum(audio2, 2);
y = audio1(14000:21000);

t = linspace(0,length(y)/Fs,length(y));
figure; plot(t,y); title('Raw Signal'); xlabel('Time(s)'); ylabel('Magnitude');

SPEC_WIN = 32;
figure; spectrogram(y,SPEC_WIN,'yaxis'); title('Raw Signal Spectrum');

SPEC_WIN = 32;
figure; spectrogram(y,SPEC_WIN,'yaxis'); title('Filtered Spectrum');

fltY = preFilter(y, true);
figure; plot(fltY); title('Summed Spectrum'); xlabel('Samples'); ylabel('Magnitude');

%%

N = 32;
H = fspecial('gaussian', [1 N], 16);
lowPass = conv(H,fltY);
lowPass = lowPass(N/2:length(lowPass));
figure; plot(lowPass); title('Filtered Transients'); xlabel('Samples'); ylabel('Magnitude');

%%
trans = transients(fltY, Fs, true);

%%
decoded = decodeBarcode(trans, true)

