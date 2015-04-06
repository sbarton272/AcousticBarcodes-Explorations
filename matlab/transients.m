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
LOW = 0;
HIGH = 1;
FALLING = 2;

LOW_HIGH_THRESH = 0.1 * std(lowPass); % this is arbitrary
FALL_HIGH_THRESH = 2;
FALL_LOW_THRESH = LOW_HIGH_THRESH;
HIGH_FALL_THRESH = 0.3;

state = LOW;
riseEdges = zeros(size(lowPass));
isInTransient = false;
minimum = lowPass(1);
maximum = 0;
for i = 1:length(lowPass)
    n = lowPass(i);
    switch state
        case LOW
            if n > LOW_HIGH_THRESH
                state = HIGH;
                riseEdges(i) = true;
            end
        case FALLING
            if n > minimum * FALL_HIGH_THRESH
                state = HIGH;
                riseEdges(i) = true;
            elseif n < FALL_LOW_THRESH
                state = LOW;
                minimum = 0;
            else
                minimum = min(minimum, n);
            end
        case HIGH
            if n < maximum * HIGH_FALL_THRESH
                state = FALLING;
                maximum = 0;
                minimum = n;
            else
                maximum = max(maximum, n);
            end
    end
end

% fltEng = lowPass > std(lowPass);
% riseEdges = diff(fltEng) > 0;


t = 1:length(y)-1;


if verbose
    figure; plot(t, y(t), t, lowPass(t), t, riseEdges(t)*max(y)); title('Transients');
    % figure; plot(t, y(t), t, lowPass(t)); title('Transients');
    % figure; plot(t, lowPass(t)); title('Transients');
end

%% Find transients

transLoc = find(riseEdges);

end
