/*
 * Description:  Small graphical user interface for the OSM importer script
 */

#ifndef OSM_IMPORTER_WINDOW_HPP
#define OSM_IMPORTER_WINDOW_HPP

#include <QtGui/QtGui>
#include <QtCore/QtCore>
#include <QtNetwork/QtNetwork>
#include <QtWidgets/QtWidgets>

class OSMImportWindow : public QMainWindow
{
  Q_OBJECT

  public:
                        OSMImportWindow(QString stringPath, QWidget *parent = 0);
    virtual            ~OSMImportWindow();

  public slots:
    void updateInputMethod();
    void selectInputFile();
    void selectConfigurationFile();
    void warnAboutThirdDimension();
    void generateWorld();
    void setProcessFinished(int exitCode, QProcess::ExitStatus exitStatus);
    void readStandardOutput();
    void readStandardError();
    void readReply();

  protected:
    void launchImporter(QString osmFile);

    QGridLayout  *mMainLayout;
    QWidget      *mCentralWidget;

    // script location
    QString       mScriptFile;

    // input method
    QGroupBox    *mInputGroupBox;
    QGridLayout  *mInputLayout;
    QRadioButton *mFileRadioButton;
    QLabel       *mFileLabel;
    QLineEdit    *mFileLineEdit;
    QPushButton  *mFilePushButton;
    QRadioButton *mCoordinateRadioButton;
    QLineEdit    *mMinLatLineEdit;
    QLineEdit    *mMaxLatLineEdit;
    QLineEdit    *mMinLongLineEdit;
    QLineEdit    *mMaxLongLineEdit;
    QLabel       *mMinLatLabel;
    QLabel       *mMaxLatLabel;
    QLabel       *mMinLongLabel;
    QLabel       *mMaxLongLabel;

    // config file
    QGroupBox    *mConfigGroupBox;
    QHBoxLayout  *mConfigHBoxLayout;
    QLineEdit    *mConfigLineEdit;
    QPushButton  *mConfigPushButton;

    // projection
    QGroupBox    *mProjectionGroupBox;
    QHBoxLayout  *mProjectionHBoxLayout;
    QLabel       *mProjectionLabel;
    QLineEdit    *mProjectionLineEdit;

    // features
    QGroupBox    *mFeaturesGroupBox;
    QVBoxLayout  *mFeaturesVBoxLayout;
    QCheckBox    *mForestsCheckBox;
    QCheckBox    *mRoadsCheckBox;
    QCheckBox    *mAreasCheckBox;
    QCheckBox    *mTreesCheckBox;
    QCheckBox    *mBarriersCheckBox;
    QCheckBox    *mRiversCheckBox;
    QCheckBox    *mBuildingsCheckBox;
    QCheckBox    *mEnableMultipolygonBuildings;
    QCheckBox    *mEnable3DCheckBox;

    // generate
    QPushButton  *mGeneratePushButton;

    // console
    QTextEdit    *mConsoleTextEdit;

    // importer process
    QProcess     *mImporterProcess;

    // reply for map acquisition
    QNetworkReply *mReply;
};

#endif // OSM_IMPORTER_WINDOW_HPP
