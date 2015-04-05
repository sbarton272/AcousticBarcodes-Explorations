function transLoc = transients(y, Fs, verbose)

transLoc = [];

%% Look at energy
y = y.^2;

%% Apply initial gaussian to do light smoothing
T = .001;
N = floor(T*Fs);
H = fspecial('gaussian', [1 N], N/8)
z = conv(H,y);

% filtered = z;

% Envelope following just like with circuit envelope following
TAU = .02 / Fs;

filtered = zeros(size(z));
time = 1;
filtered(1) = z(1);
lastMax = z(1);
for i = 2:length(z)
    % Take value if larger than falling exponential
    expVal = lastMax*exp(-TAU*time*Fs);
    if (z(i) >= expVal)
        filtered(i) = z(i);
        lastMax = z(i);
        time = 1;
    else
        filtered(i) = expVal;
        time = time + 1;
    end
end

%% Apply gaussian to reduce spurious large derivatives
% Expect clicks to be about T duration so filter for that
T = .002;
N = floor(T*Fs);

H = fspecial('gaussian', [1 N], N/8);
lowPass = conv(H,filtered);
% lowPass = filtered;

% if verbose
%     plotAudio(lowPass,Fs);
% end

%% Find transient locations
fltEng = lowPass > std(lowPass);
riseEdges = diff(fltEng) > 0;
t = 1:length(y)-1;


if verbose
    % figure; plot(t, y(t), t, lowPass(t), t, riseEdges(t)*max(y)); title('Transients');
    % figure; plot(t, y(t), t, lowPass(t)); title('Transients');
    figure; plot(t, lowPass(t)); title('Transients');
end

%% Find transients

transLoc = find(riseEdges);

end
