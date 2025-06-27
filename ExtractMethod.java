import com.github.javaparser.*;
import com.github.javaparser.ast.*;
import com.github.javaparser.ast.body.MethodDeclaration;
import java.io.FileInputStream;

public class ExtractMethod {
    public static void main(String[] args) throws Exception {
        if (args.length < 1) {
            System.out.println("Usage: java ExtractMethod <JavaFile>");
            return;
        }
        FileInputStream in = new FileInputStream(args[0]);
        JavaParser parser = new JavaParser();
        ParseResult<CompilationUnit> result = parser.parse(in);
        if (result.getResult().isPresent()) {
            CompilationUnit cu = result.getResult().get();
            cu.findAll(MethodDeclaration.class)
                    .stream()
                    .forEach(method -> System.out.println(method.toString()));
        } else {
            System.out.println("Could not parse the file.");
        }
    }
}
