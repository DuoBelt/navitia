FIND_PATH(LOG4CPLUS_INCLUDE_DIR log4cplus/logger.h PATHS "${LIB_PREFIX}/log4cplus/include")
FIND_LIBRARY(LOG4CPLUS_LIBRARY_LOG NAMES log4cplus log4cplus.dll PATHS "${LIB_PREFIX}/log4cplus/lib") 

IF(UNIX)
    FIND_LIBRARY(LOG4CPLUS_LIBRARY_PTHREAD NAMES pthread) 
ENDIF(UNIX)

IF (LOG4CPLUS_INCLUDE_DIR AND LOG4CPLUS_LIBRARY_LOG)
   SET(LOG4CPLUS_FOUND TRUE)
ENDIF (LOG4CPLUS_INCLUDE_DIR AND LOG4CPLUS_LIBRARY_LOG)

IF (LOG4CPLUS_FOUND)
   IF (NOT LOG4CPLUS_FIND_QUIETLY)
      MESSAGE(STATUS "Found log4cplus: ${LOG4CPLUS_LIBRARY_LOG}")
      IF(UNIX)
		MESSAGE(STATUS "Found pthread: ${LOG4CPLUS_LIBRARY_PTHREAD}")
        SET(LOG4CPLUS_LIBS ${LOG4CPLUS_LIBRARY_LOG} ${LOG4CPLUS_LIBRARY_PTHREAD})
      ELSE(UNIX)
        SET(LOG4CPLUS_LIBS ${LOG4CPLUS_LIBRARY_LOG})
      ENDIF(UNIX)
   ENDIF (NOT LOG4CPLUS_FIND_QUIETLY)
ELSE (LOG4CPLUS_FOUND)
   IF (LOG4CPLUS_FIND_REQUIRED)
      MESSAGE(FATAL_ERROR "Could not find log4clus")
   ENDIF (LOG4CPLUS_FIND_REQUIRED)
ENDIF (LOG4CPLUS_FOUND)

