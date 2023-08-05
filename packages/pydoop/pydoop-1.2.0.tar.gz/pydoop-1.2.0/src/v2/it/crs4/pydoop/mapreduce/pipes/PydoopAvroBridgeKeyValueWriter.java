package it.crs4.pydoop.mapreduce.pipes;

import java.util.List;
import java.util.Arrays;

import java.io.IOException;

import org.apache.hadoop.mapreduce.RecordWriter;
import org.apache.hadoop.mapreduce.TaskAttemptContext;
import org.apache.hadoop.io.Text;

import org.apache.avro.generic.GenericRecord;


public class PydoopAvroBridgeKeyValueWriter
    extends PydoopAvroBridgeWriterBase {

  public PydoopAvroBridgeKeyValueWriter(
      RecordWriter<? super GenericRecord, ? super GenericRecord> actualWriter,
      TaskAttemptContext context) {
    super(context, Submitter.AvroIO.KV);
    this.actualWriter = actualWriter;
  }

  public void write(Text key, Text value)
      throws IOException, InterruptedException {
    List<GenericRecord> outRecords = super.getOutRecords(
        Arrays.asList(key, value));
    super.write(outRecords);
  }
}
