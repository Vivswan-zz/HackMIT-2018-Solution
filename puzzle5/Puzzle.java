import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import javax.net.ssl.HttpsURLConnection;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Vector;

public class Puzzle {
    private static final String USERNAME = "Vivswan_e18564";

    private static Vector<Integer>[] getRoadMap() throws IOException {
        URLConnection request = new URL("https://gps.hackmirror.icu/api/map?user=" + Puzzle.USERNAME).openConnection();
        request.connect();
        JsonArray graph = new JsonParser().parse(new InputStreamReader((InputStream) request.getContent())).getAsJsonObject().getAsJsonArray("graph");
        Vector<Integer>[] adj = new Vector[graph.size()];
        for (int i = 0; i < graph.size(); i++) {
            adj[i] = new Vector<>();
            JsonArray item = graph.get(i).getAsJsonArray();
            for (int j = 0; j < item.size(); j++) {
                adj[i].add(item.get(j).getAsInt());
            }
        }
        return adj;
    }

    private static int getCurrentPosition(Vector<Integer>[] adj) throws IOException {
        URLConnection request = new URL("https://gps.hackmirror.icu/api/position?user=" + Puzzle.USERNAME).openConnection();
        request.connect();
        JsonObject root = new JsonParser().parse(new InputStreamReader((InputStream) request.getContent())).getAsJsonObject();
        int row = root.get("row").getAsInt();
        int col = root.get("col").getAsInt();
        return (int) (row * Math.sqrt(adj.length) + col);
    }

    private static boolean BreadthFirstSearch(Vector<Integer>[] adj, int src, int dest, int v, int[] pred, int[] dist) {
        Queue<Integer> queue = new LinkedList<>();

        boolean[] visited = new boolean[v];
        for (int i = 0; i < v; i++) {
            visited[i] = false;
            dist[i] = Integer.MAX_VALUE;
            pred[i] = -1;
        }
        visited[src] = true;
        dist[src] = 0;
        queue.add(src);

        while (!queue.isEmpty()) {
            int u = queue.peek();
            queue.remove();
            for (int i = 0; i < adj[u].size(); i++) {
                if (!visited[adj[u].elementAt(i)]) {
                    visited[adj[u].elementAt(i)] = true;
                    dist[adj[u].elementAt(i)] = dist[u] + 1;
                    pred[adj[u].elementAt(i)] = u;
                    queue.add(adj[u].elementAt(i));

                    if (adj[u].elementAt(i) == dest) {
                        return true;
                    }
                }
            }
        }

        return false;
    }

    private static String getNextMove(Vector<Integer>[] adj, int source, int destination, int numberCrossSection) {
        int[] pred = new int[numberCrossSection];
        int[] dist = new int[numberCrossSection];

        if (source == destination) {
            System.out.println("Puzzle Solved");
            return "done";
        }

        if (!BreadthFirstSearch(adj, source, destination, numberCrossSection, pred, dist)) {
            System.out.println("We are STUCK!!!!");
            System.out.println("Puzzle resetting....");
            return "stop";
        }

        Vector<Integer> path = new Vector<>();
        int crawl = destination;
        path.add(crawl);
        while (pred[crawl] != -1) {
            path.add(pred[crawl]);
            crawl = pred[crawl];
        }
        int x = path.elementAt(path.size() - 2) - path.elementAt(path.size() - 1);

        String result = "";
        if (x == 1){
            result = "right";
        } else if (x == -1){
            result = "left";
        } else if (x == 150){
            result = "down";
        } else if (x == -150){
            result = "up";
        }
        System.out.print("Path length:: " + path.size() + " : " + result + (result.equals("up") ? "\t" : "") + "\t");
        return result;
    }

    private static String sendNextMove(String move) throws IOException {
        HttpsURLConnection con = (HttpsURLConnection) new URL("https://gps.hackmirror.icu/api/move?user=" + Puzzle.USERNAME + "&move=" + move).openConnection();
        con.setRequestMethod("POST");
        con.setDoOutput(true);
        return new BufferedReader(new InputStreamReader(con.getInputStream())).readLine();
    }

    private static String func() {
        String move;
        int previousPosition = -1;
        int currentPosition;
        Vector<Integer>[] adj;
        try {
            adj = getRoadMap();
        } catch (IOException e) {
            System.out.println("Unable to load the map, please try again");
            return "stop";
        }
        while (true) {
            try {
                currentPosition = getCurrentPosition(adj);
                if (previousPosition != currentPosition) {
                    move = getNextMove(adj, currentPosition, adj.length - 1, adj.length);
                    if (move.equals("stop") || move.equals("done")) {
                        return move;
                    }
                    System.out.println(sendNextMove(move));
                    previousPosition = currentPosition;
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private static String reset() throws IOException {
        HttpsURLConnection con = (HttpsURLConnection) new URL("https://gps.hackmirror.icu/api/reset?user=" + Puzzle.USERNAME).openConnection();
        con.setRequestMethod("POST");
        con.setDoOutput(true);
        return new BufferedReader(new InputStreamReader(con.getInputStream())).readLine();
    }

    public static void main(String[] args) throws IOException {
        while (func().equals("stop")) {
            System.out.println(reset());
        }

    }
}