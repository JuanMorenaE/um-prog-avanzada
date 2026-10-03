package utilsConfig;

import java.util.Random;

public class Utils {
    public static long RandomBetween(Random random, long x, long y) {
        return random.nextLong(y - x + 1) + x;
    }
}
