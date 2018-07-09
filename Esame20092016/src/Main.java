import java.sql.*;
import java.util.*;

public class Main {

    private static Connection connection = null;

    private static void setConnection() throws SQLException {
        if (connection == null)
            connection = DriverManager.getConnection(
                "jdbc:postgresql://localhost/esami",
                "postgres",
                "postgres");
    }

    private static Set getAutostrade() throws SQLException {
        setConnection();
        String query  = "SELECT codice FROM AUTOSTRADA";
        ResultSet res = connection.prepareStatement(query).executeQuery();
        Set s = new HashSet<String>();
        while (res.next())
            s.add(res.getString("codice"));

        return s;
    }

    private static Set getComuni() throws SQLException {
        setConnection();
        String query = "SELECT codiceIstat, nome FROM COMUNE";
        ResultSet res = connection.prepareStatement(query).executeQuery();
        Set s = new HashSet<String>();
        while (res.next())
            s.add(new Comune(res.getString("codiceIstat"), res.getString("nome")));
        return s;
    }

    private static int insertTuple(String autostrada, String comune, String caselli) throws SQLException {
        setConnection();
        String update = "INSERT INTO RAGGIUNGE VALUES (?, ?, ?)";
        PreparedStatement statement = connection.prepareStatement(update);
        statement.setString(1, autostrada);
        statement.setString(2, comune);
        statement.setInt(3, Integer.parseInt(caselli));
        return statement.executeUpdate();
    }

    private static boolean contains(Set<Comune> set, String comune) {
        for (Comune c : set) {
            if (c.equals(comune))
                return true;
        }
        return false;
    }

    public static void main(String[] args) throws SQLException {
        try {
            Class.forName("org.postgresql.Driver");
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }

        Scanner scanner = new Scanner(System.in);
        Set res;
        String autostrada, comune, caselli;

        while(true) {
            System.out.print("Vuoi inserire una nuova tupla? [S/N]: ");
            String go = scanner.nextLine();
            if (go.toLowerCase().equals("s")) {
                System.out.println("Inserisci un'autostrada tra queste: ");
                res = getAutostrade();
                System.out.println(res);
                do {
                    System.out.print("> ");
                    autostrada = scanner.nextLine();
                }while (!res.contains(autostrada));

                System.out.println("Inserisci un comune tra questi: ");
                res = getComuni();
                System.out.println(res);
                do {
                    System.out.print("> ");
                    comune = scanner.nextLine();
                }while (!contains(res, comune));

                System.out.print("Inserisci il numero di caselli: ");
                caselli = scanner.nextLine();

                if (Integer.parseInt(caselli) > 0) {
                    insertTuple(autostrada, comune, caselli);
                }
                else
                    System.out.println("Si è verificato qualche errore. Riprova");
            }
            else
                System.exit(0);
        }
    }
}

final class Comune {
    private String nome;
    private String codiceIstat;

    public Comune(String codiceIstat, String nome) {
        this.nome = nome;
        this.codiceIstat = codiceIstat;
    }

    public String toString() {
        return this.codiceIstat + " " + this.nome;
    }

    @Override
    public boolean equals(Object obj) {
        return obj instanceof Comune && this.codiceIstat.equals(((Comune) obj).codiceIstat);
    }

    public boolean equals(String cod) {
        return this.codiceIstat.equals(cod);
    }

    @Override
    public int hashCode() {
        return codiceIstat.hashCode();
    }
}
