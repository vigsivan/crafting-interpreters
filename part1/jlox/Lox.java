package Lox;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

enum TokenType {
    // Single-character tokens
    LEFT_PAREN, RIGHT_PAREN, LEFT_BRACE, RIGHT_BRACE,
    COMMA, DOT, MINUS, PLUS, SEMICOLON, SLASH, STAR,

    // One or two character tokens
    BANG, BANG_EQUAL,
    EQUAL, EQUAL_EQUAL,
    GREATER, GREATER_EQUAL,
    LESS, LESS_EQUAL,

    // Literals
    IDENTIFIER, STRING, NUMBER,

    // Keywords
    AND, CLASS, ELSE, FALSE, FUN, IF, NIL, OR,
    PRINT, RETURN, SUPER, THIS, TRUE, VAR, WHILE,

    EOF
}

class Token{
    final TokenType type;
    final String lexeme;
    final Object literal;
    final int line;

    Token(TokenType type, String lexeme, Object literal, int line){
        this.type = type;
        this.lexeme = lexeme;
        this.literal = literal;
        this.line = line;
    }

    public String toString(){
        return type + " " + lexeme + " " + literal;
    }
}

public class Lox {

  static boolean hadError = false;

  public static void main(String[] args) throws IOException {
    if (args.length > 1) {
      System.out.println("Usage: jlox [script]");
      System.exit(64); 
    } else if (args.length == 1) {
      runFile(args[0]);
    } else {
      System.out.println("Running REPL");
      runPrompt();
    }
  }

  static void runFile(String arg){
      byte[] bytes = Files.readAllBytes(Paths.get(path));
      run(new String(bytes, Charset.defaultCharset()));
      if(hadError) System.exit(65);
  }

  /**
   * Runs the Lox REPL
   */
  static void runPrompt(){
      InputStreamReader input = new InputStreamReader(System.in);
      BufferedReader reader = new BufferedReader(input);

      for(;;){
          System.out.print("> ");
          String line = reader.readLine();
          if (line == null) break;
          run(line);
          hadError = false;
      }
  }

  private static void run(String source){
      Scanner scanner = new Scanner(source);
      List<Token> tokens = scanner.scanTokens();

      // TODO
      for(Token token: tokens){
          System.out.println(token);
      }
  }

  static void error(int line, String message){
      report(line, "", message);
  }

  private static void report(int line, String where, String message){
      System.err.println(
          "[line " + line + "] Error" + where + ": " + message
      );
      hadError = true;
  }
}
