-- MySQL dump 10.13  Distrib 5.5.35, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: ebid
-- ------------------------------------------------------
-- Server version	5.5.35-0ubuntu0.12.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add organization',6,'add_organization'),(17,'Can change organization',6,'change_organization'),(18,'Can delete organization',6,'delete_organization'),(19,'Can add award',7,'add_award'),(20,'Can change award',7,'change_award'),(21,'Can delete award',7,'delete_award'),(22,'Can add bid information',8,'add_bidinformation'),(23,'Can change bid information',8,'change_bidinformation'),(24,'Can delete bid information',8,'delete_bidinformation'),(25,'Can add bid line item',9,'add_bidlineitem'),(26,'Can change bid line item',9,'change_bidlineitem'),(27,'Can delete bid line item',9,'delete_bidlineitem'),(28,'Can add bidders list',10,'add_bidderslist'),(29,'Can change bidders list',10,'change_bidderslist'),(30,'Can delete bidders list',10,'delete_bidderslist'),(31,'Can add my user',11,'add_myuser'),(32,'Can change my user',11,'change_myuser'),(33,'Can delete my user',11,'delete_myuser');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2014-11-22 08:57:51',1,6,'1','My Org',1,''),(2,'2014-11-22 08:57:54',1,11,'1','root',2,'Changed org.');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'content type','contenttypes','contenttype'),(5,'session','sessions','session'),(6,'organization','ebid','organization'),(7,'award','ebid','award'),(8,'bid information','ebid','bidinformation'),(9,'bid line item','ebid','bidlineitem'),(10,'bidders list','ebid','bidderslist'),(11,'my user','ebid','myuser');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('7py77y6x4i3dijz924j9awzrdv1b7397','ZmNkMGQ2YmVkMzE0ZjMzZGE4MzVjNDg0YjY2Y2I4ZTMyYjc1ZjY2Nzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2014-12-06 08:57:25');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ebid_award`
--

LOCK TABLES `ebid_award` WRITE;
/*!40000 ALTER TABLE `ebid_award` DISABLE KEYS */;
/*!40000 ALTER TABLE `ebid_award` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ebid_bidderslist`
--

LOCK TABLES `ebid_bidderslist` WRITE;
/*!40000 ALTER TABLE `ebid_bidderslist` DISABLE KEYS */;
/*!40000 ALTER TABLE `ebid_bidderslist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ebid_bidinformation`
--

LOCK TABLES `ebid_bidinformation` WRITE;
/*!40000 ALTER TABLE `ebid_bidinformation` DISABLE KEYS */;
/*!40000 ALTER TABLE `ebid_bidinformation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ebid_bidlineitem`
--

LOCK TABLES `ebid_bidlineitem` WRITE;
/*!40000 ALTER TABLE `ebid_bidlineitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `ebid_bidlineitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ebid_myuser`
--

LOCK TABLES `ebid_myuser` WRITE;
/*!40000 ALTER TABLE `ebid_myuser` DISABLE KEYS */;
INSERT INTO `ebid_myuser` VALUES (1,'pbkdf2_sha256$12000$0WLfRutb4M0U$AbRFJX3lz1W3MO7kvPZEU7egiy9KuvUnBm6zcSP8HNY=','2014-11-22 08:57:25','root','r@r.com','','','','','2014-11-22 08:57:07','A',1);
/*!40000 ALTER TABLE `ebid_myuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ebid_organization`
--

LOCK TABLES `ebid_organization` WRITE;
/*!40000 ALTER TABLE `ebid_organization` DISABLE KEYS */;
INSERT INTO `ebid_organization` VALUES (1,'',NULL,0,'My Org','','','','','2014-11-22 08:57:51','','','','','','','','','','','','','2014-11-22 08:57:51');
/*!40000 ALTER TABLE `ebid_organization` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-11-22 17:38:16
