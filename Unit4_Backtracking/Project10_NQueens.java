/*
 * DAA Macro Project - Unit IV : Backtracking
 * Project 10 : N-Queens (N = 4) with State Space Tree tracing
 *
 * Idea : place ONE queen per row, from row 0 downwards. For every row try each
 *        column left to right. A placement is SAFE if no earlier queen shares its
 *        column or either diagonal. If a row has no safe column, BACKTRACK: remove
 *        the previous queen and try its next column.
 *
 * Every isSafe() test corresponds to one node of the state space tree
 * (root + one node per attempted placement). Unsafe nodes are pruned (red in the chart).
 *
 * Build : javac Project10_NQueens.java
 * Run   : java Project10_NQueens
 */
import java.util.ArrayList;
import java.util.List;

public class Project10_NQueens {

    static final int N = 4;
    static int[] col = new int[N];               // col[r] = column of the queen in row r
    static int nodesChecked = 0;                 // number of placements tested (tree nodes minus root)
    static int backtracks = 0;                   // number of rows that ran out of safe columns
    static List<int[]> solutions = new ArrayList<>();

    /** Is it safe to put a queen at (row, c) given queens already in rows 0..row-1? */
    static boolean isSafe(int row, int c) {
        for (int r = 0; r < row; r++) {
            if (col[r] == c) return false;                          // same column
            if (Math.abs(col[r] - c) == Math.abs(r - row)) return false; // same diagonal
        }
        return true;
    }

    static String indent(int row) {
        return "  ".repeat(row);
    }

    static void solve(int row) {
        if (row == N) {                          // all N queens placed -> a solution leaf
            solutions.add(col.clone());
            System.out.println(indent(row) + "*** SOLUTION #" + solutions.size() + " found ***");
            return;
        }
        boolean placedAny = false;
        for (int c = 0; c < N; c++) {
            nodesChecked++;
            if (isSafe(row, c)) {
                placedAny = true;
                col[row] = c;
                System.out.println(indent(row) + "Row " + row + ", col " + c + ": SAFE -> place queen");
                solve(row + 1);                  // go deeper
                System.out.println(indent(row) + "Row " + row + ", col " + c + ": remove queen (backtrack)");
            } else {
                System.out.println(indent(row) + "Row " + row + ", col " + c + ": UNSAFE -> prune (red)");
            }
        }
        if (!placedAny) backtracks++;
    }

    static void printBoard(int[] s) {
        for (int r = 0; r < N; r++) {
            StringBuilder sb = new StringBuilder("  ");
            for (int c = 0; c < N; c++) sb.append(s[r] == c ? "Q " : ". ");
            System.out.println(sb);
        }
    }

    public static void main(String[] args) {
        System.out.println("=== N-Queens by Backtracking, N = " + N + " ===");
        System.out.println("(rows and columns are numbered from 0)\n");
        System.out.println("Backtracking trace:");
        solve(0);

        System.out.println("\nTotal solutions      : " + solutions.size());
        System.out.println("Placements tested    : " + nodesChecked + " (tree nodes excluding the root)");
        System.out.println("Dead-end rows        : " + backtracks + " (rows with no safe column)");

        int k = 1;
        for (int[] s : solutions) {
            StringBuilder pos = new StringBuilder();
            for (int r = 0; r < N; r++) pos.append("(").append(r + 1).append(",").append(s[r] + 1).append(") ");
            System.out.println("\nSolution " + k++ + "  (row,col, 1-indexed): " + pos.toString().trim());
            printBoard(s);
        }
        System.out.println("\nBacktracking explained: a partial placement is abandoned the moment it "
                + "conflicts, so whole subtrees\nof the 4^4 = 256 possible full placements are never explored.");
    }
}
