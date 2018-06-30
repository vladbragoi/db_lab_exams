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

        connection.setAutoCommit(true);

        String query = "SELECT C1.nome, C1.cognome " +
                "FROM Cliente C1 " +
                "EXCEPT " +
                "SELECT C2.nome, C2.cognome " +
                "FROM Cliente C2 JOIN Noleggio N ON N.cliente = C2.nPatente " +
                "JOIN Auto A ON A.targa = N.targa " +
                "AND A.marca ILIKE ? ";

        PreparedStatement preparedStatement = connection.prepareStatement(query);

        Scanner scanner = new Scanner(System.in);
        System.out.print("Inserisci una marca: ");
        String marca = scanner.nextLine();

        preparedStatement.setString(1, marca);
        //System.out.println(preparedStatement);
        ResultSet res = preparedStatement.executeQuery();

        while (res.next()) {
            System.out.println(res.getString("nome") + " " + res.getString("cognome"));
        }
    }
}
