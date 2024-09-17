package org.example;

import java.util.concurrent.*;
import java.util.*;
import java.io.*;
import org.jfree.chart.*;
import org.jfree.chart.plot.*;
import org.jfree.data.xy.*;

public class Main {
    public static Utils.ExecutionResult straightforwardMethod(int[] arr) throws Exception {
        return Utils.timeFunction(() -> {
            long sum = 0;
            for (int value : arr) {
                sum += value;
            }
            return sum / (double) arr.length;
        });
    }

    public static Utils.ExecutionResult mapReduceMethod(int[] arr, int chunkSize) throws Exception {
        return Utils.timeFunction(() -> {
            int chunksAmount = arr.length / chunkSize;
            if (arr.length % chunkSize != 0) {
                chunksAmount += 1;
            }

            ExecutorService executor = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());
            List<Future<Long>> futures = new ArrayList<>();

            for (int i = 0; i < chunksAmount; i++) {
                int firstIndex = i * chunkSize;
                int lastIndex = Math.min(arr.length, (i + 1) * chunkSize) - 1;

                final int start = firstIndex;
                final int end = lastIndex;

                Callable<Long> callable = () -> {
                    long sum = 0;
                    for (int j = start; j <= end; j++) {
                        sum += arr[j];
                    }
                    return sum;
                };
                futures.add(executor.submit(callable));
            }

            long totalSum = 0;
            for (Future<Long> future : futures) {
                totalSum += future.get();
            }
            executor.shutdown();

            return totalSum / (double) arr.length;
        });
    }

    public static void testRange() throws Exception {
        List<Double> builtinTimes = new ArrayList<>();
        List<Double> mapReduceTimes = new ArrayList<>();
        List<Integer> sizes = new ArrayList<>();

        int maxLength = 900000000;
        int processes = 16;
        int chunkSize = maxLength / processes;
        for (int i = 1; i < maxLength; i += maxLength / 15) {
            System.out.println("Processing array size: " + i);
            sizes.add(i);
            int[] arr = Utils.generateRandomArray(i, 0, Integer.MAX_VALUE);

            Utils.ExecutionResult builtinResult = straightforwardMethod(arr);
            builtinTimes.add(builtinResult.time);

            Utils.ExecutionResult mapReduceResult = mapReduceMethod(arr, chunkSize);
            mapReduceTimes.add(mapReduceResult.time);
        }

        double[] mapReduceTimesArray = mapReduceTimes.stream().mapToDouble(Double::doubleValue).toArray();

        plotData(sizes, builtinTimes, mapReduceTimesArray, processes);

    }

    public static double average(List<Double> list) {
        double sum = 0;
        for (double d : list) {
            sum += d;
        }
        return sum / list.size();
    }

    public static void plotData(List<Integer> sizes, List<Double> builtinTimes, double[] filteredMapReduceTimes, int processes) throws IOException {
        XYSeries builtinSeries = new XYSeries("Built-in Method Time");
        for (int i = 0; i < sizes.size(); i++) {
            builtinSeries.add(sizes.get(i).doubleValue(), builtinTimes.get(i));
        }

        XYSeries mapReduceSeries = new XYSeries("Map-Reduce Method Time (Filtered)");
        int len = Math.min(sizes.size(), filteredMapReduceTimes.length);
        for (int i = 0; i < len; i++) {
            mapReduceSeries.add(sizes.get(i).doubleValue(), filteredMapReduceTimes[i]);
        }

        XYSeriesCollection dataset = new XYSeriesCollection();
        dataset.addSeries(builtinSeries);
        dataset.addSeries(mapReduceSeries);

        JFreeChart chart = ChartFactory.createXYLineChart(
                "Execution Time: Built-in Method vs Map-Reduce Method",
                "Array Size",
                "Execution Time (seconds)",
                dataset,
                PlotOrientation.VERTICAL,
                true,
                true,
                false
        );

        XYPlot plot = chart.getXYPlot();
        plot.setDomainGridlinesVisible(true);
        plot.setRangeGridlinesVisible(true);

        long currentTime = System.currentTimeMillis() / 1000;
        String filename = "execution_time_comparison_p" + processes + "_" + currentTime + ".png";

        ChartUtils.saveChartAsPNG(new File(filename), chart, 800, 600);
        System.out.println("Plot saved as " + filename);
    }

    public static void main(String[] args) throws Exception {
        testRange();
    }
}
