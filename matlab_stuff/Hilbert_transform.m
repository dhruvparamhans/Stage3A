samp = 1/0.01;
x=-10:1/samp:10;
norm = normpdf(x,0,2.0);
sinx1 = norm.*sin(pi*x);
sinx2 = norm.*sin(pi*x+2.7);
figure; 
plot(x,sinx1,'r',x,sinx2,'b');
y1 = hilbert(sinx1);
y2 = hilbert(sinx2);
p1 = angle(y1);
p2 = angle(y2);
p = unwrap(p1) - unwrap(p2); 
figure;
subplot(211); 
plot(x, p1, 'r', x, p2, 'b'); 
title('Angles');
subplot(212); 
plot(p);
title('Phase Difference');

instfreq1 = samp/(2*pi)*diff(unwrap(p1));
instfreq2 = samp/(2*pi)*diff(unwrap(p2));
figure; 
plot(instfreq1);
hold on; 
plot(instfreq2);
hold off; 
title('Instantaneous Frequency');

% Now we shall calculate the stuff from the envelope and phase
% information 

envelope1 = abs(y1);
envelope2 = abs(y2);

phase1 = phase(y1);
phase2 = phase(y2);

figure;
subplot(211);
plot(x,phase1, 'r', x, phase2, 'b');
subplot(212);
plot(x, cos(phase1), 'r', x', cos(phase2), 'b');

figure;
plot(p);
hold on;
plot(phase1-phase2);
hold off;








