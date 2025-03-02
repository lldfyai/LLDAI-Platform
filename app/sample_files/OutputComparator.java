import java.util.Iterator;
import java.util.Properties;

public class OutputComparator {
  public static boolean compareOutputs(int testCaseNum, String actualOutput, Iterator<String> expectedIterator, Properties resultsProps) {
    StringBuilder expectedOutput = new StringBuilder();
    String line;

    while (expectedIterator.hasNext() && !(line = expectedIterator.next()).isEmpty()) {
      expectedOutput.append(line).append("\n");
    }
    String expectedOutputString = expectedOutput.toString().trim();
    if (expectedOutputString.equals(actualOutput)) {
      return true;
    } else {
      resultsProps.setProperty("actualOutput", actualOutput);
      resultsProps.setProperty("expectedOutput", expectedOutputString);
      return false;
    }
  }
}