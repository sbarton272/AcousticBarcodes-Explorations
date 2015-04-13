function transLoc = transients(y, Fs, verbose)

transLoc = [];

%% Look at power
y = y .^ 2;

%% Apply initial gaussian to do light smoothing
T = .0002;
N = floor(T*Fs);
H = fspecial('gaussian', [1 N], N/8);
lowPass = conv(H,y);

if verbose
    figure; plot(y, 'g'); title('LP 1');
    hold on; plot(lowPass);
end

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

t = 1:length(y)-1;

if verbose
    figure; plot(t, y(t), t, lowPass(t), t, riseEdges(t)*max(lowPass));
    title('Transients');
end

%% Find transients

transLoc = find(riseEdges);

end
