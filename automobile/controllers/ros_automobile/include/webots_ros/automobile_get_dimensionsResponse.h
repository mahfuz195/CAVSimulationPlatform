#ifndef WEBOTS_ROS_MESSAGE_AUTOMOBILE_GET_DIMENSIONSRESPONSE_H
#define WEBOTS_ROS_MESSAGE_AUTOMOBILE_GET_DIMENSIONSRESPONSE_H


#include <string>
#include <vector>
#include <map>

#include "ros/types.h"
#include "ros/serialization.h"
#include "ros/builtin_message_traits.h"
#include "ros/message_operations.h"



namespace webots_ros
{
template <class ContainerAllocator>
struct automobile_get_dimensionsResponse_
{
  typedef automobile_get_dimensionsResponse_<ContainerAllocator> Type;

  automobile_get_dimensionsResponse_()
    : trackFront(0.0)
    , trackRear(0.0)
    , wheelBase(0.0)
    , frontWheelRadius(0.0)
    , rearWheelRadius(0.0)  {
    }
  automobile_get_dimensionsResponse_(const ContainerAllocator& _alloc)
    : trackFront(0.0)
    , trackRear(0.0)
    , wheelBase(0.0)
    , frontWheelRadius(0.0)
    , rearWheelRadius(0.0)  {
    }


   typedef double  _trackFront_type;
  _trackFront_type trackFront;

   typedef double  _trackRear_type;
  _trackRear_type trackRear;

   typedef double  _wheelBase_type;
  _wheelBase_type wheelBase;

   typedef double  _frontWheelRadius_type;
  _frontWheelRadius_type frontWheelRadius;

   typedef double  _rearWheelRadius_type;
  _rearWheelRadius_type rearWheelRadius;




  typedef boost::shared_ptr< ::webots_ros::automobile_get_dimensionsResponse_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::webots_ros::automobile_get_dimensionsResponse_<ContainerAllocator> const> ConstPtr;
  boost::shared_ptr<std::map<std::string, std::string> > __connection_header;

};

typedef ::webots_ros::automobile_get_dimensionsResponse_<std::allocator<void> > automobile_get_dimensionsResponse;

typedef boost::shared_ptr< ::webots_ros::automobile_get_dimensionsResponse > automobile_get_dimensionsResponsePtr;
typedef boost::shared_ptr< ::webots_ros::automobile_get_dimensionsResponse const> automobile_get_dimensionsResponseConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::webots_ros::automobile_get_dimensionsResponse_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::webots_ros::automobile_get_dimensionsResponse_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace webots_ros

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': True, 'IsMessage': True, 'HasHeader': False}
// {'std_msgs': ['/opt/ros/groovy/share/std_msgs/msg'], 'webots_ros': ['/home/simon/my_Webots_Projects/controllers/ros_controller/catkin_ws/src/webots_ros/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::webots_ros::automobile_get_dimensionsResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::webots_ros::automobile_get_dimensionsResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::webots_ros::automobile_get_dimensionsResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::webots_ros::automobile_get_dimensionsResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::webots_ros::automobile_get_dimensionsResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::webots_ros::automobile_get_dimensionsResponse_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::webots_ros::automobile_get_dimensionsResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "3cc904008b725304e06b1ad175139ee0";
  }

  static const char* value(const ::webots_ros::automobile_get_dimensionsResponse_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x0147e4f36cba5cdaULL;
  static const uint64_t static_value2 = 0x7fa39c089e493413ULL;
};

template<class ContainerAllocator>
struct DataType< ::webots_ros::automobile_get_dimensionsResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "webots_ros/automobile_get_dimensionsResponse";
  }

  static const char* value(const ::webots_ros::automobile_get_dimensionsResponse_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::webots_ros::automobile_get_dimensionsResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "float64 trackFront\n\
float64 trackRear\n\
float64 wheelBase\n\
float64 frontWheelRadius\n\
float64 rearWheelRadius\n\\n\
\n\
";
  }

  static const char* value(const ::webots_ros::automobile_get_dimensionsResponse_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::webots_ros::automobile_get_dimensionsResponse_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
            stream.next(m.trackFront);
      stream.next(m.trackRear);
      stream.next(m.wheelBase);
      stream.next(m.frontWheelRadius);
      stream.next(m.rearWheelRadius);

    }

    ROS_DECLARE_ALLINONE_SERIALIZER;
  };

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::webots_ros::automobile_get_dimensionsResponse_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::webots_ros::automobile_get_dimensionsResponse_<ContainerAllocator>& v)
  {
        s << indent << "trackFront: ";
    Printer<double>::stream(s, indent + "  ", v.trackFront);
    s << indent << "trackRear: ";
    Printer<double>::stream(s, indent + "  ", v.trackRear);
    s << indent << "wheelBase: ";
    Printer<double>::stream(s, indent + "  ", v.wheelBase);
    s << indent << "frontWheelRadius: ";
    Printer<double>::stream(s, indent + "  ", v.frontWheelRadius);
    s << indent << "rearWheelRadius: ";
    Printer<double>::stream(s, indent + "  ", v.rearWheelRadius);

  }
};

} // namespace message_operations
} // namespace ros

#endif // WEBOTS_ROS_MESSAGE_AUTOMOBILE_GET_DIMENSIONSRESPONSE_H
