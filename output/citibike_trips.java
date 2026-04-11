// ORM class for table 'citibike_trips'
// WARNING: This class is AUTO-GENERATED. Modify at your own risk.
//
// Debug information:
// Generated date: Sat Apr 11 21:29:29 MSK 2026
// For connector: org.apache.sqoop.manager.PostgresqlManager
import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.mapred.lib.db.DBWritable;
import org.apache.sqoop.lib.JdbcWritableBridge;
import org.apache.sqoop.lib.DelimiterSet;
import org.apache.sqoop.lib.FieldFormatter;
import org.apache.sqoop.lib.RecordParser;
import org.apache.sqoop.lib.BooleanParser;
import org.apache.sqoop.lib.BlobRef;
import org.apache.sqoop.lib.ClobRef;
import org.apache.sqoop.lib.LargeObjectLoader;
import org.apache.sqoop.lib.SqoopRecord;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.CharBuffer;
import java.sql.Date;
import java.sql.Time;
import java.sql.Timestamp;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.HashMap;

public class citibike_trips extends SqoopRecord  implements DBWritable, Writable {
  private final int PROTOCOL_VERSION = 3;
  public int getClassFormatVersion() { return PROTOCOL_VERSION; }
  public static interface FieldSetterCommand {    void setField(Object value);  }  protected ResultSet __cur_result_set;
  private Map<String, FieldSetterCommand> setters = new HashMap<String, FieldSetterCommand>();
  private void init0() {
    setters.put("ride_id", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        citibike_trips.this.ride_id = (String)value;
      }
    });
    setters.put("rideable_type", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        citibike_trips.this.rideable_type = (String)value;
      }
    });
    setters.put("started_at", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        citibike_trips.this.started_at = (java.sql.Timestamp)value;
      }
    });
    setters.put("ended_at", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        citibike_trips.this.ended_at = (java.sql.Timestamp)value;
      }
    });
    setters.put("start_station_name", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        citibike_trips.this.start_station_name = (String)value;
      }
    });
    setters.put("start_station_id", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        citibike_trips.this.start_station_id = (String)value;
      }
    });
    setters.put("end_station_name", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        citibike_trips.this.end_station_name = (String)value;
      }
    });
    setters.put("end_station_id", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        citibike_trips.this.end_station_id = (String)value;
      }
    });
    setters.put("start_lat", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        citibike_trips.this.start_lat = (Double)value;
      }
    });
    setters.put("start_lng", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        citibike_trips.this.start_lng = (Double)value;
      }
    });
    setters.put("end_lat", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        citibike_trips.this.end_lat = (Double)value;
      }
    });
    setters.put("end_lng", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        citibike_trips.this.end_lng = (Double)value;
      }
    });
    setters.put("member_casual", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        citibike_trips.this.member_casual = (String)value;
      }
    });
  }
  public citibike_trips() {
    init0();
  }
  private String ride_id;
  public String get_ride_id() {
    return ride_id;
  }
  public void set_ride_id(String ride_id) {
    this.ride_id = ride_id;
  }
  public citibike_trips with_ride_id(String ride_id) {
    this.ride_id = ride_id;
    return this;
  }
  private String rideable_type;
  public String get_rideable_type() {
    return rideable_type;
  }
  public void set_rideable_type(String rideable_type) {
    this.rideable_type = rideable_type;
  }
  public citibike_trips with_rideable_type(String rideable_type) {
    this.rideable_type = rideable_type;
    return this;
  }
  private java.sql.Timestamp started_at;
  public java.sql.Timestamp get_started_at() {
    return started_at;
  }
  public void set_started_at(java.sql.Timestamp started_at) {
    this.started_at = started_at;
  }
  public citibike_trips with_started_at(java.sql.Timestamp started_at) {
    this.started_at = started_at;
    return this;
  }
  private java.sql.Timestamp ended_at;
  public java.sql.Timestamp get_ended_at() {
    return ended_at;
  }
  public void set_ended_at(java.sql.Timestamp ended_at) {
    this.ended_at = ended_at;
  }
  public citibike_trips with_ended_at(java.sql.Timestamp ended_at) {
    this.ended_at = ended_at;
    return this;
  }
  private String start_station_name;
  public String get_start_station_name() {
    return start_station_name;
  }
  public void set_start_station_name(String start_station_name) {
    this.start_station_name = start_station_name;
  }
  public citibike_trips with_start_station_name(String start_station_name) {
    this.start_station_name = start_station_name;
    return this;
  }
  private String start_station_id;
  public String get_start_station_id() {
    return start_station_id;
  }
  public void set_start_station_id(String start_station_id) {
    this.start_station_id = start_station_id;
  }
  public citibike_trips with_start_station_id(String start_station_id) {
    this.start_station_id = start_station_id;
    return this;
  }
  private String end_station_name;
  public String get_end_station_name() {
    return end_station_name;
  }
  public void set_end_station_name(String end_station_name) {
    this.end_station_name = end_station_name;
  }
  public citibike_trips with_end_station_name(String end_station_name) {
    this.end_station_name = end_station_name;
    return this;
  }
  private String end_station_id;
  public String get_end_station_id() {
    return end_station_id;
  }
  public void set_end_station_id(String end_station_id) {
    this.end_station_id = end_station_id;
  }
  public citibike_trips with_end_station_id(String end_station_id) {
    this.end_station_id = end_station_id;
    return this;
  }
  private Double start_lat;
  public Double get_start_lat() {
    return start_lat;
  }
  public void set_start_lat(Double start_lat) {
    this.start_lat = start_lat;
  }
  public citibike_trips with_start_lat(Double start_lat) {
    this.start_lat = start_lat;
    return this;
  }
  private Double start_lng;
  public Double get_start_lng() {
    return start_lng;
  }
  public void set_start_lng(Double start_lng) {
    this.start_lng = start_lng;
  }
  public citibike_trips with_start_lng(Double start_lng) {
    this.start_lng = start_lng;
    return this;
  }
  private Double end_lat;
  public Double get_end_lat() {
    return end_lat;
  }
  public void set_end_lat(Double end_lat) {
    this.end_lat = end_lat;
  }
  public citibike_trips with_end_lat(Double end_lat) {
    this.end_lat = end_lat;
    return this;
  }
  private Double end_lng;
  public Double get_end_lng() {
    return end_lng;
  }
  public void set_end_lng(Double end_lng) {
    this.end_lng = end_lng;
  }
  public citibike_trips with_end_lng(Double end_lng) {
    this.end_lng = end_lng;
    return this;
  }
  private String member_casual;
  public String get_member_casual() {
    return member_casual;
  }
  public void set_member_casual(String member_casual) {
    this.member_casual = member_casual;
  }
  public citibike_trips with_member_casual(String member_casual) {
    this.member_casual = member_casual;
    return this;
  }
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (!(o instanceof citibike_trips)) {
      return false;
    }
    citibike_trips that = (citibike_trips) o;
    boolean equal = true;
    equal = equal && (this.ride_id == null ? that.ride_id == null : this.ride_id.equals(that.ride_id));
    equal = equal && (this.rideable_type == null ? that.rideable_type == null : this.rideable_type.equals(that.rideable_type));
    equal = equal && (this.started_at == null ? that.started_at == null : this.started_at.equals(that.started_at));
    equal = equal && (this.ended_at == null ? that.ended_at == null : this.ended_at.equals(that.ended_at));
    equal = equal && (this.start_station_name == null ? that.start_station_name == null : this.start_station_name.equals(that.start_station_name));
    equal = equal && (this.start_station_id == null ? that.start_station_id == null : this.start_station_id.equals(that.start_station_id));
    equal = equal && (this.end_station_name == null ? that.end_station_name == null : this.end_station_name.equals(that.end_station_name));
    equal = equal && (this.end_station_id == null ? that.end_station_id == null : this.end_station_id.equals(that.end_station_id));
    equal = equal && (this.start_lat == null ? that.start_lat == null : this.start_lat.equals(that.start_lat));
    equal = equal && (this.start_lng == null ? that.start_lng == null : this.start_lng.equals(that.start_lng));
    equal = equal && (this.end_lat == null ? that.end_lat == null : this.end_lat.equals(that.end_lat));
    equal = equal && (this.end_lng == null ? that.end_lng == null : this.end_lng.equals(that.end_lng));
    equal = equal && (this.member_casual == null ? that.member_casual == null : this.member_casual.equals(that.member_casual));
    return equal;
  }
  public boolean equals0(Object o) {
    if (this == o) {
      return true;
    }
    if (!(o instanceof citibike_trips)) {
      return false;
    }
    citibike_trips that = (citibike_trips) o;
    boolean equal = true;
    equal = equal && (this.ride_id == null ? that.ride_id == null : this.ride_id.equals(that.ride_id));
    equal = equal && (this.rideable_type == null ? that.rideable_type == null : this.rideable_type.equals(that.rideable_type));
    equal = equal && (this.started_at == null ? that.started_at == null : this.started_at.equals(that.started_at));
    equal = equal && (this.ended_at == null ? that.ended_at == null : this.ended_at.equals(that.ended_at));
    equal = equal && (this.start_station_name == null ? that.start_station_name == null : this.start_station_name.equals(that.start_station_name));
    equal = equal && (this.start_station_id == null ? that.start_station_id == null : this.start_station_id.equals(that.start_station_id));
    equal = equal && (this.end_station_name == null ? that.end_station_name == null : this.end_station_name.equals(that.end_station_name));
    equal = equal && (this.end_station_id == null ? that.end_station_id == null : this.end_station_id.equals(that.end_station_id));
    equal = equal && (this.start_lat == null ? that.start_lat == null : this.start_lat.equals(that.start_lat));
    equal = equal && (this.start_lng == null ? that.start_lng == null : this.start_lng.equals(that.start_lng));
    equal = equal && (this.end_lat == null ? that.end_lat == null : this.end_lat.equals(that.end_lat));
    equal = equal && (this.end_lng == null ? that.end_lng == null : this.end_lng.equals(that.end_lng));
    equal = equal && (this.member_casual == null ? that.member_casual == null : this.member_casual.equals(that.member_casual));
    return equal;
  }
  public void readFields(ResultSet __dbResults) throws SQLException {
    this.__cur_result_set = __dbResults;
    this.ride_id = JdbcWritableBridge.readString(1, __dbResults);
    this.rideable_type = JdbcWritableBridge.readString(2, __dbResults);
    this.started_at = JdbcWritableBridge.readTimestamp(3, __dbResults);
    this.ended_at = JdbcWritableBridge.readTimestamp(4, __dbResults);
    this.start_station_name = JdbcWritableBridge.readString(5, __dbResults);
    this.start_station_id = JdbcWritableBridge.readString(6, __dbResults);
    this.end_station_name = JdbcWritableBridge.readString(7, __dbResults);
    this.end_station_id = JdbcWritableBridge.readString(8, __dbResults);
    this.start_lat = JdbcWritableBridge.readDouble(9, __dbResults);
    this.start_lng = JdbcWritableBridge.readDouble(10, __dbResults);
    this.end_lat = JdbcWritableBridge.readDouble(11, __dbResults);
    this.end_lng = JdbcWritableBridge.readDouble(12, __dbResults);
    this.member_casual = JdbcWritableBridge.readString(13, __dbResults);
  }
  public void readFields0(ResultSet __dbResults) throws SQLException {
    this.ride_id = JdbcWritableBridge.readString(1, __dbResults);
    this.rideable_type = JdbcWritableBridge.readString(2, __dbResults);
    this.started_at = JdbcWritableBridge.readTimestamp(3, __dbResults);
    this.ended_at = JdbcWritableBridge.readTimestamp(4, __dbResults);
    this.start_station_name = JdbcWritableBridge.readString(5, __dbResults);
    this.start_station_id = JdbcWritableBridge.readString(6, __dbResults);
    this.end_station_name = JdbcWritableBridge.readString(7, __dbResults);
    this.end_station_id = JdbcWritableBridge.readString(8, __dbResults);
    this.start_lat = JdbcWritableBridge.readDouble(9, __dbResults);
    this.start_lng = JdbcWritableBridge.readDouble(10, __dbResults);
    this.end_lat = JdbcWritableBridge.readDouble(11, __dbResults);
    this.end_lng = JdbcWritableBridge.readDouble(12, __dbResults);
    this.member_casual = JdbcWritableBridge.readString(13, __dbResults);
  }
  public void loadLargeObjects(LargeObjectLoader __loader)
      throws SQLException, IOException, InterruptedException {
  }
  public void loadLargeObjects0(LargeObjectLoader __loader)
      throws SQLException, IOException, InterruptedException {
  }
  public void write(PreparedStatement __dbStmt) throws SQLException {
    write(__dbStmt, 0);
  }

  public int write(PreparedStatement __dbStmt, int __off) throws SQLException {
    JdbcWritableBridge.writeString(ride_id, 1 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(rideable_type, 2 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeTimestamp(started_at, 3 + __off, 93, __dbStmt);
    JdbcWritableBridge.writeTimestamp(ended_at, 4 + __off, 93, __dbStmt);
    JdbcWritableBridge.writeString(start_station_name, 5 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(start_station_id, 6 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(end_station_name, 7 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(end_station_id, 8 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeDouble(start_lat, 9 + __off, 8, __dbStmt);
    JdbcWritableBridge.writeDouble(start_lng, 10 + __off, 8, __dbStmt);
    JdbcWritableBridge.writeDouble(end_lat, 11 + __off, 8, __dbStmt);
    JdbcWritableBridge.writeDouble(end_lng, 12 + __off, 8, __dbStmt);
    JdbcWritableBridge.writeString(member_casual, 13 + __off, 12, __dbStmt);
    return 13;
  }
  public void write0(PreparedStatement __dbStmt, int __off) throws SQLException {
    JdbcWritableBridge.writeString(ride_id, 1 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(rideable_type, 2 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeTimestamp(started_at, 3 + __off, 93, __dbStmt);
    JdbcWritableBridge.writeTimestamp(ended_at, 4 + __off, 93, __dbStmt);
    JdbcWritableBridge.writeString(start_station_name, 5 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(start_station_id, 6 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(end_station_name, 7 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(end_station_id, 8 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeDouble(start_lat, 9 + __off, 8, __dbStmt);
    JdbcWritableBridge.writeDouble(start_lng, 10 + __off, 8, __dbStmt);
    JdbcWritableBridge.writeDouble(end_lat, 11 + __off, 8, __dbStmt);
    JdbcWritableBridge.writeDouble(end_lng, 12 + __off, 8, __dbStmt);
    JdbcWritableBridge.writeString(member_casual, 13 + __off, 12, __dbStmt);
  }
  public void readFields(DataInput __dataIn) throws IOException {
this.readFields0(__dataIn);  }
  public void readFields0(DataInput __dataIn) throws IOException {
    if (__dataIn.readBoolean()) { 
        this.ride_id = null;
    } else {
    this.ride_id = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.rideable_type = null;
    } else {
    this.rideable_type = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.started_at = null;
    } else {
    this.started_at = new Timestamp(__dataIn.readLong());
    this.started_at.setNanos(__dataIn.readInt());
    }
    if (__dataIn.readBoolean()) { 
        this.ended_at = null;
    } else {
    this.ended_at = new Timestamp(__dataIn.readLong());
    this.ended_at.setNanos(__dataIn.readInt());
    }
    if (__dataIn.readBoolean()) { 
        this.start_station_name = null;
    } else {
    this.start_station_name = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.start_station_id = null;
    } else {
    this.start_station_id = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.end_station_name = null;
    } else {
    this.end_station_name = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.end_station_id = null;
    } else {
    this.end_station_id = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.start_lat = null;
    } else {
    this.start_lat = Double.valueOf(__dataIn.readDouble());
    }
    if (__dataIn.readBoolean()) { 
        this.start_lng = null;
    } else {
    this.start_lng = Double.valueOf(__dataIn.readDouble());
    }
    if (__dataIn.readBoolean()) { 
        this.end_lat = null;
    } else {
    this.end_lat = Double.valueOf(__dataIn.readDouble());
    }
    if (__dataIn.readBoolean()) { 
        this.end_lng = null;
    } else {
    this.end_lng = Double.valueOf(__dataIn.readDouble());
    }
    if (__dataIn.readBoolean()) { 
        this.member_casual = null;
    } else {
    this.member_casual = Text.readString(__dataIn);
    }
  }
  public void write(DataOutput __dataOut) throws IOException {
    if (null == this.ride_id) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, ride_id);
    }
    if (null == this.rideable_type) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, rideable_type);
    }
    if (null == this.started_at) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.started_at.getTime());
    __dataOut.writeInt(this.started_at.getNanos());
    }
    if (null == this.ended_at) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.ended_at.getTime());
    __dataOut.writeInt(this.ended_at.getNanos());
    }
    if (null == this.start_station_name) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, start_station_name);
    }
    if (null == this.start_station_id) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, start_station_id);
    }
    if (null == this.end_station_name) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, end_station_name);
    }
    if (null == this.end_station_id) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, end_station_id);
    }
    if (null == this.start_lat) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeDouble(this.start_lat);
    }
    if (null == this.start_lng) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeDouble(this.start_lng);
    }
    if (null == this.end_lat) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeDouble(this.end_lat);
    }
    if (null == this.end_lng) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeDouble(this.end_lng);
    }
    if (null == this.member_casual) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, member_casual);
    }
  }
  public void write0(DataOutput __dataOut) throws IOException {
    if (null == this.ride_id) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, ride_id);
    }
    if (null == this.rideable_type) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, rideable_type);
    }
    if (null == this.started_at) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.started_at.getTime());
    __dataOut.writeInt(this.started_at.getNanos());
    }
    if (null == this.ended_at) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.ended_at.getTime());
    __dataOut.writeInt(this.ended_at.getNanos());
    }
    if (null == this.start_station_name) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, start_station_name);
    }
    if (null == this.start_station_id) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, start_station_id);
    }
    if (null == this.end_station_name) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, end_station_name);
    }
    if (null == this.end_station_id) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, end_station_id);
    }
    if (null == this.start_lat) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeDouble(this.start_lat);
    }
    if (null == this.start_lng) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeDouble(this.start_lng);
    }
    if (null == this.end_lat) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeDouble(this.end_lat);
    }
    if (null == this.end_lng) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeDouble(this.end_lng);
    }
    if (null == this.member_casual) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, member_casual);
    }
  }
  private static final DelimiterSet __outputDelimiters = new DelimiterSet((char) 44, (char) 10, (char) 0, (char) 0, false);
  public String toString() {
    return toString(__outputDelimiters, true);
  }
  public String toString(DelimiterSet delimiters) {
    return toString(delimiters, true);
  }
  public String toString(boolean useRecordDelim) {
    return toString(__outputDelimiters, useRecordDelim);
  }
  public String toString(DelimiterSet delimiters, boolean useRecordDelim) {
    StringBuilder __sb = new StringBuilder();
    char fieldDelim = delimiters.getFieldsTerminatedBy();
    __sb.append(FieldFormatter.escapeAndEnclose(ride_id==null?"null":ride_id, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(rideable_type==null?"null":rideable_type, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(started_at==null?"null":"" + started_at, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(ended_at==null?"null":"" + ended_at, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(start_station_name==null?"null":start_station_name, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(start_station_id==null?"null":start_station_id, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(end_station_name==null?"null":end_station_name, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(end_station_id==null?"null":end_station_id, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(start_lat==null?"null":"" + start_lat, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(start_lng==null?"null":"" + start_lng, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(end_lat==null?"null":"" + end_lat, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(end_lng==null?"null":"" + end_lng, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(member_casual==null?"null":member_casual, delimiters));
    if (useRecordDelim) {
      __sb.append(delimiters.getLinesTerminatedBy());
    }
    return __sb.toString();
  }
  public void toString0(DelimiterSet delimiters, StringBuilder __sb, char fieldDelim) {
    __sb.append(FieldFormatter.escapeAndEnclose(ride_id==null?"null":ride_id, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(rideable_type==null?"null":rideable_type, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(started_at==null?"null":"" + started_at, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(ended_at==null?"null":"" + ended_at, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(start_station_name==null?"null":start_station_name, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(start_station_id==null?"null":start_station_id, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(end_station_name==null?"null":end_station_name, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(end_station_id==null?"null":end_station_id, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(start_lat==null?"null":"" + start_lat, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(start_lng==null?"null":"" + start_lng, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(end_lat==null?"null":"" + end_lat, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(end_lng==null?"null":"" + end_lng, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(member_casual==null?"null":member_casual, delimiters));
  }
  private static final DelimiterSet __inputDelimiters = new DelimiterSet((char) 44, (char) 10, (char) 0, (char) 0, false);
  private RecordParser __parser;
  public void parse(Text __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(CharSequence __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(byte [] __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(char [] __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(ByteBuffer __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(CharBuffer __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  private void __loadFromFields(List<String> fields) {
    Iterator<String> __it = fields.listIterator();
    String __cur_str = null;
    try {
    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.ride_id = null; } else {
      this.ride_id = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.rideable_type = null; } else {
      this.rideable_type = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.started_at = null; } else {
      this.started_at = java.sql.Timestamp.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.ended_at = null; } else {
      this.ended_at = java.sql.Timestamp.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.start_station_name = null; } else {
      this.start_station_name = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.start_station_id = null; } else {
      this.start_station_id = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.end_station_name = null; } else {
      this.end_station_name = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.end_station_id = null; } else {
      this.end_station_id = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.start_lat = null; } else {
      this.start_lat = Double.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.start_lng = null; } else {
      this.start_lng = Double.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.end_lat = null; } else {
      this.end_lat = Double.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.end_lng = null; } else {
      this.end_lng = Double.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.member_casual = null; } else {
      this.member_casual = __cur_str;
    }

    } catch (RuntimeException e) {    throw new RuntimeException("Can't parse input data: '" + __cur_str + "'", e);    }  }

  private void __loadFromFields0(Iterator<String> __it) {
    String __cur_str = null;
    try {
    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.ride_id = null; } else {
      this.ride_id = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.rideable_type = null; } else {
      this.rideable_type = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.started_at = null; } else {
      this.started_at = java.sql.Timestamp.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.ended_at = null; } else {
      this.ended_at = java.sql.Timestamp.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.start_station_name = null; } else {
      this.start_station_name = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.start_station_id = null; } else {
      this.start_station_id = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.end_station_name = null; } else {
      this.end_station_name = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.end_station_id = null; } else {
      this.end_station_id = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.start_lat = null; } else {
      this.start_lat = Double.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.start_lng = null; } else {
      this.start_lng = Double.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.end_lat = null; } else {
      this.end_lat = Double.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.end_lng = null; } else {
      this.end_lng = Double.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.member_casual = null; } else {
      this.member_casual = __cur_str;
    }

    } catch (RuntimeException e) {    throw new RuntimeException("Can't parse input data: '" + __cur_str + "'", e);    }  }

  public Object clone() throws CloneNotSupportedException {
    citibike_trips o = (citibike_trips) super.clone();
    o.started_at = (o.started_at != null) ? (java.sql.Timestamp) o.started_at.clone() : null;
    o.ended_at = (o.ended_at != null) ? (java.sql.Timestamp) o.ended_at.clone() : null;
    return o;
  }

  public void clone0(citibike_trips o) throws CloneNotSupportedException {
    o.started_at = (o.started_at != null) ? (java.sql.Timestamp) o.started_at.clone() : null;
    o.ended_at = (o.ended_at != null) ? (java.sql.Timestamp) o.ended_at.clone() : null;
  }

  public Map<String, Object> getFieldMap() {
    Map<String, Object> __sqoop$field_map = new HashMap<String, Object>();
    __sqoop$field_map.put("ride_id", this.ride_id);
    __sqoop$field_map.put("rideable_type", this.rideable_type);
    __sqoop$field_map.put("started_at", this.started_at);
    __sqoop$field_map.put("ended_at", this.ended_at);
    __sqoop$field_map.put("start_station_name", this.start_station_name);
    __sqoop$field_map.put("start_station_id", this.start_station_id);
    __sqoop$field_map.put("end_station_name", this.end_station_name);
    __sqoop$field_map.put("end_station_id", this.end_station_id);
    __sqoop$field_map.put("start_lat", this.start_lat);
    __sqoop$field_map.put("start_lng", this.start_lng);
    __sqoop$field_map.put("end_lat", this.end_lat);
    __sqoop$field_map.put("end_lng", this.end_lng);
    __sqoop$field_map.put("member_casual", this.member_casual);
    return __sqoop$field_map;
  }

  public void getFieldMap0(Map<String, Object> __sqoop$field_map) {
    __sqoop$field_map.put("ride_id", this.ride_id);
    __sqoop$field_map.put("rideable_type", this.rideable_type);
    __sqoop$field_map.put("started_at", this.started_at);
    __sqoop$field_map.put("ended_at", this.ended_at);
    __sqoop$field_map.put("start_station_name", this.start_station_name);
    __sqoop$field_map.put("start_station_id", this.start_station_id);
    __sqoop$field_map.put("end_station_name", this.end_station_name);
    __sqoop$field_map.put("end_station_id", this.end_station_id);
    __sqoop$field_map.put("start_lat", this.start_lat);
    __sqoop$field_map.put("start_lng", this.start_lng);
    __sqoop$field_map.put("end_lat", this.end_lat);
    __sqoop$field_map.put("end_lng", this.end_lng);
    __sqoop$field_map.put("member_casual", this.member_casual);
  }

  public void setField(String __fieldName, Object __fieldVal) {
    if (!setters.containsKey(__fieldName)) {
      throw new RuntimeException("No such field:"+__fieldName);
    }
    setters.get(__fieldName).setField(__fieldVal);
  }

}
