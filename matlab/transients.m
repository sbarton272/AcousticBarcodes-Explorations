function transLoc = transients(y, Fs)

transLoc = [];

%% Look at energy
y = y.^2;

%% Low pass to get idea of where changes are
% Expect clicks to be about T duration so filter for that
T = .003;
N = floor(T*Fs);

H = fspecial('gaussian', [1 N], N/8);
lowPass = conv(H,abs(y));

plotAudio(lowPass,Fs);

%% Check gaussian
%t = floor(.3325*Fs):floor(.34*Fs);
%h = [H zeros(1,length(t) - length(H))];
%figure; plot(t,y(t),t,h,t,lowPass(t));

%% Find transient locations
lowPassEng = lowPass > std(lowPass);
riseEdges = diff(lowPassEng) > 0;
t = 1:length(y)-1;
figure; plot(t, y(t), t, lowPass(t), t, riseEdges(t)*max(y)); title('Transients');

%% Find transients

transLoc = find(riseEdges);

end
