class Calculator:

    CONVERSION_FACTOR = 250

    def cubicWeight(self, length, height, width):
        lengthCm = float(length) / 100
        heightCm = float(height) / 100
        widthCm = float(width) / 100
        volume = lengthCm * heightCm * widthCm
        weightKg = volume * self.CONVERSION_FACTOR
        weightG = weightKg * 1000
        return weightG
