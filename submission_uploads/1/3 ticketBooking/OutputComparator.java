import java.util.*;

public class OutputComparator {
    public static boolean compareOutputs(String actual, String expected) {
        String[] actualLines = actual.trim().split("\\r?\\n");
        String[] expectedLines = expected.trim().split("\\r?\\n");
        
        if (actualLines.length != expectedLines.length) {
            return false;
        }
        
        for (int i = 0; i < actualLines.length; i++) {
            if (!actualLines[i].trim().equals(expectedLines[i].trim())) {
                return false;
            }
        }
        return true;
    }
}
