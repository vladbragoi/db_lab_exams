import java.sql.*;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) throws SQLException {
        try {
            Class.forName("org.postgresql.Driver");
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }

        Connection connection = DriverManager.getConnection(
                "jdbc:postgresql://localhost/esami",
                "postgres",
                "postgres");

        String query = "SELECT R.nome, R.tempoPreparazione as tempo " +
                "FROM Ricetta R " +
                    "JOIN Composizione C ON C.ricetta = R.id " +
                    "JOIN Ingrediente I ON C.ingrediente = I.id " +
                "WHERE R.regione ILIKE ? " +
                    "AND I.carboidrati > 40";
        PreparedStatement preparedStatement = connection.prepareStatement(query);
        Scanner scanner = new Scanner(System.in);
        System.out.print("Inserisci una regione: ");
        String regione = scanner.nextLine();

        preparedStatement.setString(1, regione);

        ResultSet res = preparedStatement.executeQuery();

        while(res.next()) {
            System.out.println(res.getString("nome") + " "
                         + res.getString("tempo"));
        }
    }
}
