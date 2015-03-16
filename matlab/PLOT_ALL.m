
clear all
close all

[audioFiles, Fs] = loadAudio();

for i = 1:length(audioFiles)
   plotAudio(audioFiles{i}.audio,Fs); 
   audioFiles{i}.name
   pause
end