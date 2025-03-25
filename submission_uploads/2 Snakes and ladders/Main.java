import java.io.*;
import java.util.*;
import java.nio.file.*;

public class Main {
    public static void main(String[] args) throws Exception {
        // Capture output using ByteArrayOutputStream
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        PrintStream ps = new PrintStream(baos);
        PrintStream oldOut = System.out;
        System.setOut(ps);

        // Read input from standard input (or via file redirection)
        Scanner sc = new Scanner(System.in);
        List<String> testCaseLines = new ArrayList<>();
        List<List<String>> testCases = new ArrayList<>();

        while (sc.hasNextLine()) {
            String line = sc.nextLine().trim();
            if (line.isEmpty()) {
                if (!testCaseLines.isEmpty()) {
                    testCases.add(new ArrayList<>(testCaseLines));
                    testCaseLines.clear();
                }
            } else {
                testCaseLines.add(line);
            }
        }
        if (!testCaseLines.isEmpty()) {
            testCases.add(new ArrayList<>(testCaseLines));
        }
        
        // Process each test case using Driver
        for (List<String> testCase : testCases) {
            Driver driver = new Driver();
            driver.processTestCase(testCase);
            System.out.println(); // Separate outputs of different test cases with a blank line
        }
        sc.close();

        // Flush and capture actual output
        System.out.flush();
        String actualOutput = baos.toString();
        System.setOut(oldOut);

        // Read expected output from Output.txt
        String expectedOutput = new String(Files.readAllBytes(Paths.get("Output.txt")));

        // Compare outputs using OutputComparator
        if (OutputComparator.compareOutputs(actualOutput, expectedOutput)) {
            System.out.println("Outputs match. Test passed!");
        } else {
            System.out.println("Outputs do not match. Test failed.");
        }
    }
}
