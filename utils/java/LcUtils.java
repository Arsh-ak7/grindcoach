// utils/java/LcUtils.java
package utils.java;

import java.util.*;

public class LcUtils {
    public static class ListNode {
        public int val;
        public ListNode next;

        public ListNode() {}
        public ListNode(int val) { this.val = val; }
        public ListNode(int val, ListNode next) { this.val = val; this.next = next; }
    }

    public static class TreeNode {
        public int val;
        public TreeNode left;
        public TreeNode right;

        public TreeNode() {}
        public TreeNode(int val) { this.val = val; }
        public TreeNode(int val, TreeNode left, TreeNode right) {
            this.val = val;
            this.left = left;
            this.right = right;
        }
    }

    // --- Helper for Debugging ---
    public static void debug(Object... args) {
        System.err.print("\033[34m[DEBUG] ");
        for (Object arg : args) {
            if (arg instanceof int[]) {
                System.err.print(Arrays.toString((int[]) arg) + " ");
            } else if (arg instanceof Object[]) {
                System.err.print(Arrays.deepToString((Object[]) arg) + " ");
            } else {
                System.err.print(arg + " ");
            }
        }
        System.err.println("\033[0m");
    }
}
