/****************************************************************************
** Meta object code from reading C++ file 'OSMImportWindow.hpp'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.9.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../OSMImportWindow.hpp"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'OSMImportWindow.hpp' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.9.1. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_OSMImportWindow_t {
    QByteArrayData data[14];
    char stringdata0[220];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_OSMImportWindow_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_OSMImportWindow_t qt_meta_stringdata_OSMImportWindow = {
    {
QT_MOC_LITERAL(0, 0, 15), // "OSMImportWindow"
QT_MOC_LITERAL(1, 16, 17), // "updateInputMethod"
QT_MOC_LITERAL(2, 34, 0), // ""
QT_MOC_LITERAL(3, 35, 15), // "selectInputFile"
QT_MOC_LITERAL(4, 51, 23), // "selectConfigurationFile"
QT_MOC_LITERAL(5, 75, 23), // "warnAboutThirdDimension"
QT_MOC_LITERAL(6, 99, 13), // "generateWorld"
QT_MOC_LITERAL(7, 113, 18), // "setProcessFinished"
QT_MOC_LITERAL(8, 132, 8), // "exitCode"
QT_MOC_LITERAL(9, 141, 20), // "QProcess::ExitStatus"
QT_MOC_LITERAL(10, 162, 10), // "exitStatus"
QT_MOC_LITERAL(11, 173, 18), // "readStandardOutput"
QT_MOC_LITERAL(12, 192, 17), // "readStandardError"
QT_MOC_LITERAL(13, 210, 9) // "readReply"

    },
    "OSMImportWindow\0updateInputMethod\0\0"
    "selectInputFile\0selectConfigurationFile\0"
    "warnAboutThirdDimension\0generateWorld\0"
    "setProcessFinished\0exitCode\0"
    "QProcess::ExitStatus\0exitStatus\0"
    "readStandardOutput\0readStandardError\0"
    "readReply"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_OSMImportWindow[] = {

 // content:
       7,       // revision
       0,       // classname
       0,    0, // classinfo
       9,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: name, argc, parameters, tag, flags
       1,    0,   59,    2, 0x0a /* Public */,
       3,    0,   60,    2, 0x0a /* Public */,
       4,    0,   61,    2, 0x0a /* Public */,
       5,    0,   62,    2, 0x0a /* Public */,
       6,    0,   63,    2, 0x0a /* Public */,
       7,    2,   64,    2, 0x0a /* Public */,
      11,    0,   69,    2, 0x0a /* Public */,
      12,    0,   70,    2, 0x0a /* Public */,
      13,    0,   71,    2, 0x0a /* Public */,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int, 0x80000000 | 9,    8,   10,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,

       0        // eod
};

void OSMImportWindow::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        OSMImportWindow *_t = static_cast<OSMImportWindow *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->updateInputMethod(); break;
        case 1: _t->selectInputFile(); break;
        case 2: _t->selectConfigurationFile(); break;
        case 3: _t->warnAboutThirdDimension(); break;
        case 4: _t->generateWorld(); break;
        case 5: _t->setProcessFinished((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< QProcess::ExitStatus(*)>(_a[2]))); break;
        case 6: _t->readStandardOutput(); break;
        case 7: _t->readStandardError(); break;
        case 8: _t->readReply(); break;
        default: ;
        }
    }
}

const QMetaObject OSMImportWindow::staticMetaObject = {
    { &QMainWindow::staticMetaObject, qt_meta_stringdata_OSMImportWindow.data,
      qt_meta_data_OSMImportWindow,  qt_static_metacall, nullptr, nullptr}
};


const QMetaObject *OSMImportWindow::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *OSMImportWindow::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_OSMImportWindow.stringdata0))
        return static_cast<void*>(const_cast< OSMImportWindow*>(this));
    return QMainWindow::qt_metacast(_clname);
}

int OSMImportWindow::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QMainWindow::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 9)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 9;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 9)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 9;
    }
    return _id;
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
