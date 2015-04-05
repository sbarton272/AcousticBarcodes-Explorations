function transLoc = transients(y, Fs, verbose)

transLoc = [];

%% Look at energy
y = y.^2;

%% Envelope following just like with circuit envelope following
TAU = .1 / Fs;

filtered = zeros(size(y));
time = 1;
filtered(1) = y(1);
lastMax = y(1);
for i = 2:length(y)
    % Take value if larger than falling exponential
    expVal = lastMax*exp(-TAU*time*Fs);
    if (y(i) >= expVal)
        filtered(i) = y(i);
        lastMax = y(i);
        time = 1;
    else
        filtered(i) = expVal;
        time = time + 1;
    end
end

%% Apply gaussian to reduce spurious large derivatives
% Expect clicks to be about T duration so filter for that
T = .001;
N = floor(T*Fs);

H = fspecial('gaussian', [1 N], N/8);
lowPass = conv(H,filtered);

if verbose
    plotAudio(lowPass,Fs);
end

%% Find transient locations
fltEng = lowPass > std(lowPass);
riseEdges = diff(fltEng) > 0;
t = 1:length(y)-1;
figure; plot(t, y(t), t, lowPass(t), t, riseEdges(t)*max(y)); title('Transients');

%% Find transients

transLoc = find(riseEdges);

end
