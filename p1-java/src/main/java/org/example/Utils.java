package org.example;

import java.util.Random;
import java.util.concurrent.Callable;

public class Utils {

    public static int[] generateRandomArray(int size, int minElement, int maxElement) {
        int[] arr = new int[size];
        Random rand = new Random();
        int bound = maxElement - minElement;
        for (int i = 0; i < size; i++) {
            arr[i] = rand.nextInt(bound) + minElement;
        }
        return arr;
    }

    public static ExecutionResult timeFunction(Callable<Double> func) throws Exception {
        long startTime = System.nanoTime();
        double result = func.call();
        long endTime = System.nanoTime();
        double executionTime = (endTime - startTime) / 1e9;
        return new ExecutionResult(result, executionTime);
    }

    public static class ExecutionResult {
        public double result;
        public double time;

        public ExecutionResult(double result, double time) {
            this.result = result;
            this.time = time;
        }
    }
}
