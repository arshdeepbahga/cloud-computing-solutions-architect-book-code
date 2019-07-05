package com.mycompany.app; 
import backtype.storm.Config; 
import backtype.storm.LocalCluster; 
import backtype.storm.StormSubmitter; 
import backtype.storm.task.ShellBolt; 
import backtype.storm.spout.ShellSpout; 
import backtype.storm.topology.IRichBolt; 
import backtype.storm.topology.IRichSpout; 
import backtype.storm.topology.OutputFieldsDeclarer; 
import backtype.storm.topology.TopologyBuilder; 
import backtype.storm.tuple.Fields; 
import java.util.Map; 
 
 
public class App { 
 
public static class SensorSpout extends ShellSpout implements IRichSpout { 
    public SensorSpout() { 
        super("python", "myspout.py"); 
    } 
 
    @Override 
    public void declareOutputFields(OutputFieldsDeclarer declarer) { 
        declarer.declare(new Fields("word")); 
    } 
 
    @Override 
    public Map<String, Object> getComponentConfiguration() { 
        return null; 
    } 
} 
 
public static class SensorBolt extends ShellBolt implements IRichBolt { 
    public SensorBolt() { 
        super("python", "mybolt.py"); 
    } 
 
    @Override 
    public void declareOutputFields(OutputFieldsDeclarer declarer) { 
        declarer.declare(new Fields("word")); 
    } 
 
    @Override 
    public Map<String, Object> getComponentConfiguration() { 
        return null; 
    } 
} 
 
 
public static void main(String[] args) throws Exception { 
 
    TopologyBuilder builder = new TopologyBuilder(); 
 
    builder.setSpout("spout", new SensorSpout(), 5); 
    builder.setBolt("analysis", 
            new SensorBolt(), 8).shuffleGrouping("spout"); 
 
    Config conf = new Config(); 
    conf.setDebug(true); 
 
    if (args != null && args.length > 0) { 
        conf.setNumWorkers(3); 
        StormSubmitter.submitTopology(args[0], conf, 
            builder.createTopology()); 
    } 
    else { 
        conf.setMaxTaskParallelism(3); 
 
        LocalCluster cluster = new LocalCluster(); 
        cluster.submitTopology("mytopology", conf, 
            builder.createTopology()); 
 
        Thread.sleep(10000); 
 
        cluster.shutdown(); 
    } 
} 
 
}
