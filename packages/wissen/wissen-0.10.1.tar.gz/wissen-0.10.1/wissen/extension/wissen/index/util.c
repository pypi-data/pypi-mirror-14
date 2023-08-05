#include <math.h>
#include <stdio.h>

#define PI_180 0.017453292519943295
#define E 2.7182818284590451

double log2 (double d) {
	if (d == 0.0) return 0.0;
	return log (d) / log (2.0);
}

double factorial (double n) {	
	double f = 0;
	for (; n; f += n--)	{
	}
	return f;
}

double odds (int tf, int size, int n) {
	double odds, prob;
	prob = (double)tf / (double)size;	
	if (prob == 0.0) {
		odds = (1.0 / pow ((double)n, 2)) / (1.0 - 1.0 / pow ((double)n, 2));
	}
	else if (prob == 1.0) {
		odds = (1.0 - 1.0 / pow ((double)n, 2)) / (1.0 / pow ((double)n, 2));
	}
	else {
		odds = prob / (1.0 - prob);
	}
	return odds;
}

double mdistance (double baselat, double baselong, double otherlat, double otherlong) {
	double dLat1InRad, dLong1InRad, dLat2InRad, dLong2InRad;
	double dLongitude, dLatitude;
	double d, a, c;
	const double EarthRadiusMeters = 6376500;

  dLat1InRad = baselat * PI_180;
  dLong1InRad = baselong * PI_180;
  dLat2InRad = otherlat * PI_180;
  dLong2InRad = otherlong * PI_180;

  dLongitude = dLong2InRad - dLong1InRad;
  dLatitude = dLat2InRad - dLat1InRad;

  a = pow(sin(dLatitude / 2.0), 2.0) +
          cos(dLat1InRad) * cos(dLat2InRad) *
          pow(sin(dLongitude / 2.0), 2.0);
  c = 2.0 * atan2(sqrt(a), sqrt(1.0 - a));
  d = EarthRadiusMeters * c;

  return d;
}
