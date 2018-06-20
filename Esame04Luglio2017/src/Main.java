import org.postgresql.util.PGInterval;

import java.sql.*;

public class Main{

    public static void main(String[] args) throws SQLException {
        try {
            Class.forName("org.postgresql.Driver");
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
        String codiceFiscale = args [0];
        String idBiblio = args [1];

        Connection connection = DriverManager.getConnection("localhost", "postgres", "postgres");

        String query = "SELECT idRisorsa as id, dataInizio as data, durata " +
                        "FROM PRESTITO " +
                        "WHERE idBiblioteca = ? " +
                            "AND idUtente = ?";

        PreparedStatement statement = connection.prepareStatement(query);
        statement.setString(1, idBiblio);
        statement.setString(2, codiceFiscale);

        ResultSet res = statement.executeQuery();

        System.out.println("RESULT: ");
        while(res.next()) {
            System.out.println(String.format("| %20 s | %20 s | %20 s |", res.getInt("idRisorsa") ,
                    res.getDate("dataInizio"),
                    ((PGInterval) res.getObject("durata")).getValue()));
        }
    }
}