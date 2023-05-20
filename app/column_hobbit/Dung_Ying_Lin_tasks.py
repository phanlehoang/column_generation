import numpy as np
import arc
import gurobipy as gp
from gurobipy import GRB
from csp_wizard.node import Node

from time_constraint_shortest_path_solver import TimeConstraintShortestPathSolver
from time_constraint_shortest_path_solver_ver2 import TimeConstraintShortestPathSolverVer2
# Tạo task
from bus_wizard.task import Task
task1 = Task(1, 340, 450)
task2 = Task(2, 340, 420)
task3 = Task(3, 345, 435)
task4 = Task(4, 345, 435)
task5 = Task(5, 350, 480)
task6 = Task(6, 360, 466)
task7 = Task(7, 360, 530)
task8 = Task(8, 360, 515)
task9 = Task(9, 360, 481)
task10 = Task(10, 360, 450)

task11 = Task(11, 365, 475)
task12 = Task(12, 370, 490)
task13 = Task(13, 370, 545)
task14 = Task(14, 375, 465)
task15 = Task(15, 375, 470)
task16 = Task(16, 380, 485)
task17 = Task(17, 385, 481)
task18 = Task(18, 390, 485)
task19 = Task(19, 405, 505)
task20 = Task(20, 410, 515)

task21 = Task(21, 415, 550)
task22 = Task(22, 430, 526)
task23 = Task(23, 430, 520)
task24 = Task(24, 430, 535)
task25 = Task(25, 450, 525)
task26 = Task(26, 460, 580)
task27 = Task(27, 460, 585)
task28 = Task(28, 470, 588)
task29 = Task(29, 475, 610)
task30 = Task(30, 495, 618)

task31 = Task(31, 500, 596)
task32 = Task(32, 500, 630)
task33 = Task(33, 500, 570)
task34 = Task(34, 500, 590)
task35 = Task(35, 505, 601)
task36 = Task(36, 510, 600)
task37 = Task(37, 520, 610)
task38 = Task(38, 530, 580)
task39 = Task(39, 540, 695)
task40 = Task(40, 540, 625)

task41 = Task(41, 545, 641)
task42 = Task(42, 560, 650)
task43 = Task(43, 560, 650)
task44 = Task(44, 560, 630)
task45 = Task(45, 562, 722)
task46 = Task(46, 570, 666)
task47 = Task(47, 585, 686)
task48 = Task(48, 592, 752)
task49 = Task(49, 595, 725)
task50 = Task(50, 600, 650)

task51 = Task(51, 600, 701)
task52 = Task(52, 615, 735)
task53 = Task(53, 615, 740)
task54 = Task(54, 615, 738)
task55 = Task(55, 625, 721)
task56 = Task(56, 640, 740)
task57 = Task(57, 640, 770)
task58 = Task(58, 640, 775)
task59 = Task(59, 640, 725)
task60 = Task(60, 660, 761)

task61 = Task(61, 660, 745)
task62 = Task(62, 665, 785)
task63 = Task(63, 680, 785)
task64 = Task(64, 680, 760)
task65 = Task(65, 680, 810)
task66 = Task(66, 680, 781)
task67 = Task(67, 700, 796)
task68 = Task(68, 705, 828)
task69 = Task(69, 720, 820)
task70 = Task(70, 720, 820)

task71 = Task(71, 720, 821)
task72 = Task(72, 725, 810)
task73 = Task(73, 730, 855)
task74 = Task(74, 740, 836)
task75 = Task(75, 742, 902)
task76 = Task(76, 750, 873)
task77 = Task(77, 750, 851)
task78 = Task(78, 760, 860)
task79 = Task(79, 765, 885)
task80 = Task(80, 770, 840)

task81 = Task(81, 772, 932)
task82 = Task(82, 775, 905)
task83 = Task(83, 780, 876)
task84 = Task(84, 780, 850)
task85 = Task(85, 780, 886)
task86 = Task(86, 790, 915)
task87 = Task(87, 795, 918)
task88 = Task(88, 800, 900)
task89 = Task(89, 800, 930)
task90 = Task(90, 800, 870)

task91 = Task(91, 802, 962)
task92 = Task(92, 810, 906)
task93 = Task(93, 810, 965)
task94 = Task(94, 815, 870)
task95 = Task(95, 815, 935)
task96 = Task(96, 815, 950)
task97 = Task(97, 820, 921)
task98 = Task(98, 830, 960)
task99 = Task(99, 830, 915)
task100 = Task(100, 832, 992)

task101 = Task(101, 840, 920)
task102 = Task(102, 840, 936)
task103 = Task(103, 840, 960)
task104 = Task(104, 840, 965)
task105 = Task(105, 840, 930)
task106 = Task(106, 840, 941)
task107 = Task(107, 840, 930)
task108 = Task(108, 852, 1012)
task109 = Task(109, 860, 990)
task110 = Task(110, 865, 961)

task111 = Task(111, 865, 1095)
task112 = Task(112, 870, 970)
task113 = Task(113, 870, 955)
task114 = Task(114, 880, 976)
task115 = Task(115, 890, 960)
task116 = Task(116, 890, 986)
task117 = Task(117, 900, 935)
task118 = Task(118, 900, 990)
task119 = Task(119, 900, 1015)
task120 = Task(120, 900, 970)

task121 = Task(121, 902, 1067)
task122 = Task(122, 920, 1035)
task123 = Task(123, 930, 1030)
task124 = Task(124, 932, 1112)
task125 = Task(125, 940, 1025)
task126 = Task(126, 940, 1036)
task127 = Task(127, 950, 1073)
task128 = Task(128, 950, 1045)
task129 = Task(129, 955, 1095)
task130 = Task(130, 960, 1060)

task131 = Task(131, 960, 1056)
task132 = Task(132, 960, 995)
task133 = Task(133, 960, 1060)
task134 = Task(134, 965, 1115)
task135 = Task(135, 972, 1117)
task136 = Task(136, 980, 1095)
task137 = Task(137, 990, 1105)
task138 = Task(138, 990, 1075)
task139 = Task(139, 996, 1141)
task140 = Task(140, 1000, 1125)

task141 = Task(141, 1000, 1110)
task142 = Task(142, 1000, 1126)
task143 = Task(143, 1010, 1120)
task144 = Task(144, 1020, 1130)
task145 = Task(145, 1020, 1165)
task146 = Task(146, 1020, 1135)
task147 = Task(147, 1020, 1135)
task148 = Task(148, 1020, 1135)
task149 = Task(149, 1020, 1135)
task150 = Task(150, 1020, 1135)

task151 = Task(151, 1020, 1135)
task152 = Task(152, 1020, 1135)
task153 = Task(153, 1020, 1135)
task154 = Task(154, 1020, 1135)
task155 = Task(155, 1020, 1135)
task156 = Task(156, 1020, 1135)
task157 = Task(157, 1020, 1135)
task158 = Task(158, 1020, 1135)
task159 = Task(159, 1020, 1135)
task160 = Task(160, 1020, 1135)

task161 = Task(161, 1020, 1135)
task162 = Task(162, 1020, 1135)
task163 = Task(163, 1020, 1135)
task164 = Task(164, 1020, 1135)
task165 = Task(165, 1020, 1135)
task166 = Task(166, 1020, 1135)
task167 = Task(167, 1020, 1135)
task168 = Task(168, 1020, 1135)
task169 = Task(169, 1020, 1135)
task170 = Task(170, 1020, 1135)

task171 = Task(171, 1020, 1135)
task172 = Task(172, 1020, 1135)
task173 = Task(173, 1020, 1135)
task174 = Task(174, 1020, 1135)
task175 = Task(175, 1020, 1135)
task176 = Task(176, 1020, 1135)
task177 = Task(177, 1020, 1135)
task178 = Task(178, 1020, 1135)
task179 = Task(179, 1020, 1135)
task180 = Task(180, 1020, 1135)

task181 = Task(181, 1020, 1135)
task182 = Task(182, 1020, 1135)
task183 = Task(183, 1020, 1135)
task184 = Task(184, 1020, 1135)
task185 = Task(185, 1020, 1135)
task186 = Task(186, 1020, 1135)
task187 = Task(187, 1020, 1135)
task188 = Task(188, 1020, 1135)
task189 = Task(189, 1020, 1135)
task190 = Task(190, 1020, 1135)

tasks = [task1, task2, task3, task4, task5, task6, task7, task8, task9, task10, task11, task12, task13,
         task14, task15, task16, task17, task18, task19, task20, task21, task22, task23, task24, task25,
         task26, task27, task28, task29, task30, task31, task32, task33, task34, task35, task36, task37,
         task38, task39, task40, task41, task42, task43, task44, task45, task46, task47, task48, task49,
         task50, task51, task52, task53, task54, task55, task56, task57, task58, task59, task60, task61,
         task62, task63, task64, task65, task66, task67, task68, task69, task70, task71, task72, task73,
         task74, task75, task76, task77, task78, task79, task80, task81, task82, task83, task84, task85,
         task86, task87, task88, task89, task90, task91, task92, task93, task94, task95, task96, task97,
         task98, task99, task100, task101, task102, task103, task104, task105, task106, task107, task108,
         task109, task110, task111, task112, task113, task114, task115, task116, task117, task118, task119,
         task120, task121, task122, task123, task124, task125, task126, task127, task128, task129, task130,
         task131, task132, task133, task134, task135, task136, task137, task138, task139, task140, task141,
         task142, task143, task144, task145, task146, task147, task148, task149, task150, task151, task152,
         task153, task154, task155, task156, task157, task158, task159, task160, task161, task162, task163,
         task164, task165, task166, task167, task168, task169, task170, task171, task172, task173, task174,
         task175, task176, task177, task178, task179, task180, task181, task182, task183, task184, task185,
         task186, task187, task188, task189, task190]

def Dung_Ying_Lin_tasks():
    return tasks





