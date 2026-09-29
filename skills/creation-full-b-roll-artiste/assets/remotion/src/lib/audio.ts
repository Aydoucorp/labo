// Conversion decibels -> gain lineaire (amplitude).
export const dbToGain = (db: number): number => {
  if (!Number.isFinite(db)) {
    return 1;
  }
  return Math.pow(10, db / 20);
};
