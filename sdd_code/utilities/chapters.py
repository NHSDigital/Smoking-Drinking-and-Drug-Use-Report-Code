import sdd_code.utilities.parameters as param
from sdd_code.utilities import tables


def get_chapters():
    """
    Establishes each of the output files, sheets and associated table processes
    required for each chapter
    Add or remove any from the list as required

    Parameters:
        None
    Returns:
        Filepath, sheetnames and function to be run for each table

    """
    all_chapters = [
        {
            "output_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_drinkprev_source.xlsx",
            "table_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_drinkprev_datatables_master.xlsx",
            "run_chapter": param.CHAPTER_DRINKING_PREVALANCE,
            "chapter_number": "5",
            "sheets": [
                {
                    "name": "Ever_Drank",
                    "content": [tables.create_breakdown_dgender_age1115_region_ethnicgp5_alevr]
                },
                {
                    "name": "Last_Drank",
                    "content": [tables.create_breakdown_dgender_age1115_region_ethnicgp5_dallast5]
                },
                {
                    "name": "Day_Drank",
                    "content": [tables.create_breakdown_dgender_age1315_daysdrank]
                },
                {
                    "name": "Units_LastWk",
                    "content": [tables.create_breakdown_dgender_age1315_nal7utg7]
                },
                {
                    "name": "Drink_Freq",
                    "content": [tables.create_breakdown_dgender_age1115_dalfrq7]
                },
                {
                    "name": "Stats_Sex_Age1315",
                    "content": [
                        tables.create_breakdown_stats_dgender_age1315_nal7,
                        tables.create_breakdown_stats_dgender_age1315_al7
                        ]
                },
                {
                    "name": "Age_First_Drunk",
                    "content": [tables.create_breakdown_dgender_dalagedru]
                },
                {
                    "name": "Drank_Drunk_Ever",
                    "content": [tables.create_breakdown_dgender_age1115_daldrunk]
                },
                {
                    "name": "Drank_Drunk_Last4Wk",
                    "content": [tables.create_breakdown_dgender_age1115_dal4dru5]
                },
                {
                    "name": "Type_Total_LastWk",
                    "content": [tables.create_breakdown_dgender_typedrank]
                },
                {
                    "name": "Days_LastWk",
                    "content": [tables.create_breakdown_dgender_age1315_dal7day]
                },
                {
                    "name": "Age_First_Drank",
                    "content": [tables.create_breakdown_dgender_dagedrank]
                },
                {
                    "name": "Type_LastWk",
                    "content": [tables.create_breakdown_dgender_age1315_dal7]
                },
                {
                    "name": "Units_DrinkDays",
                    "content": [tables.create_breakdown_dgender_age1315_dalunitsday]
                },
            ],
        },
        {
            "output_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_youngwhodrink_source.xlsx",
            "table_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_youngwhodrink_datatables_master.xlsx",
            "run_chapter": param.CHAPTER_YOUNG_WHO_DRINK,
            "chapter_number": "6",
            "sheets": [
                {
                    "name": "Drank4Wks_TimesDrunk",
                    "content": [tables.create_breakdown_dgender_age1315_dal4dru5]
                 },
                {
                    "name": "HowObtain_All",
                    "content": [tables.create_breakdown_alcohol_howobtain_all]
                 },
                {
                    "name": "HowObtain",
                    "content": [tables.create_breakdown_alcohol_howobtain]
                 },
                {
                    "name": "WhereBuy",
                    "content": [tables.create_breakdown_dgender_age1215_nal7ut_wherebuy]
                 },
                {
                    "name": "WhereDrink",
                    "content": [tables.create_breakdown_dgender_age1215_nal7ut_wheredrink]
                 },
                {
                    "name": "Drunk4Wks_Tried",
                    "content": [tables.create_breakdown_dgender_age1315_al4wdedr]
                },
                {
                    "name": "Drunk4Wks_Adverse",
                    "content": [tables.create_breakdown_dgender_dal4dru5_drunkadverse]
                },
                {
                    "name": "WhoDrink",
                    "content": [tables.create_breakdown_dgender_age1215_nal7ut_whodrink]
                 },
                {
                    "name": "Fam_LastDr_LivesWith",
                    "content": [tables.create_breakdown_dallast3_dalfamknw]
                 },
                {
                    "name": "Buy_WhereBuy",
                    "content": [tables.create_breakdown_age1315_alcohol_buywherebuy]
                },
            ],
        },
        {
            "output_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_drinkcontext_source.xlsx",
            "table_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_drinkcontext_datatables_master.xlsx",
            "run_chapter": param.CHAPTER_DRINK_CONTEXT,
            "chapter_number": "7",
            "sheets": [
                {
                    "name": "ParentAttitude",
                    "content": [tables.create_breakdown_dgender_age1115_dallast_nal7ut_dalfam]
                 },
                {
                    "name": "ParentAttitude_Current",
                    "content": [tables.create_breakdown_dalfamknw_dalfam]
                 },
                {
                    "name": "DrunkLast4wk",
                    "content": [tables.create_breakdown_dalfam_dal4dru5]
                 },
                {
                    "name": "Attitudes",
                    "content": [tables.create_breakdown_dgender_age1115_dallast_attitudes]
                 },
                {
                    "name": "Attitudes_DrunkLast4wk",
                    "content": [tables.create_breakdown_dal4dru_attitudes]
                },
                {
                    "name": "LastDrank",
                    "content": [tables.create_breakdown_dalfam_dfasbands_imdquin_dallast3]
                },
                {
                    "name": "LastDrankAll",
                    "content": [tables.create_breakdown_dfasbands_imdquin_dallast3]
                },
            ],
        },
        {
            "output_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_schoollessons_source.xlsx",
            "table_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_schoollessons_datatables_master.xlsx",
            "run_chapter": param.CHAPTER_SCHOOL_LESSONS,
            "chapter_number": "12",
            "sheets": [
                {
                    "name": "PupilLessons",
                    "content": [tables.create_breakdown_dgender_syear_puplessons]
                 },
                {
                    "name": "EnoughInfo",
                    "content": [tables.create_breakdown_dgender_syear_info]
                 },
                {
                    "name": "SchoolLessons",
                    "content": [tables.create_breakdown_schlessons],
                    "teacher_table": True
                 },
                {
                    "name": "WhoContributes",
                    "content": [tables.create_breakdown_contributes],
                    "teacher_table": True
                 },
                {
                    "name": "LessonResources",
                    "content": [tables.create_breakdown_sources],
                    "teacher_table": True
                 },
                {
                    "name": "OtherAdvice",
                    "content": [tables.create_breakdown_otheradvice],
                    "teacher_table": True
                },
                {
                    "name": "LessonsSmoking",
                    "content": [tables.create_breakdown_lessonssmoking],
                    "teacher_table": True
                },
                {
                    "name": "LessonsDrinking",
                    "content": [tables.create_breakdown_lessonsdrinking],
                    "teacher_table": True
                },
                {
                    "name": "LessonsDrugs",
                    "content": [tables.create_breakdown_lessonsdrugs],
                    "teacher_table": True
                },
            ],
        },
        {
            "output_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_smokingprev_source.xlsx",
            "table_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_smokingprev_datatables_master.xlsx",
            "run_chapter": param.CHAPTER_SMOKING_PREVALANCE,
            "chapter_number": "1", 
            "sheets": [
                {
                    "name": "SmokingStatus",
                    "content": [tables.create_breakdown_dgender_age_region_ethnicgp5_dcgstg5]
                },
                {
                    "name": "SmokedLastWeek",
                    "content": [tables.create_breakdown_dgender_age_cg7]
                },
                {
                    "name": "CigLastWeek",
                    "content": [tables.create_breakdown_dcgstg5_dcg7totg]
                },
                {
                    "name": "DaysLastWeek",
                    "content": [tables.create_breakdown_dcgstg3_dcg7day]
                },
                {
                    "name": "Stats_Current",
                    "content": [tables.create_breakdown_stats_dgender_dcgstg3_dcg7tot]
                },
                {
                   "name": "Stats_SmokedLastWeek",
                   "content": [tables.create_breakdown_stats_dgender_dcgstg3_cg7]
                },
            ],
        },
        {
            "output_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_youngwhosmoke_source.xlsx",
            "table_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_youngwhosmoke_datatables_master.xlsx",
            "run_chapter": param.CHAPTER_YOUNG_WHO_SMOKE,
            "chapter_number": "2",
            "sheets": [
                {
                    "name": "SourceShops",
                    "content": [tables.create_breakdown_shops_wherebuy]
                },
                {
                    "name": "DifficultBuyShops",
                    "content": [tables.create_breakdown_age1315_cgdiff]
                },
                {
                    "name": "SourceCurrent",
                    "content": [tables.create_breakdown_dcgstg3_dgender_age1315_cgsourcecurr]
                },
                {
                    "name": "SourceRegular",
                    "content": [tables.create_breakdown_cgsourcereg]
                },
                {
                    "name": "LengthTime",
                    "content": [tables.create_breakdown_dgender_cglong]
                },
                {
                    "name": "DiffQuit",
                    "content": [tables.create_breakdown_cgstopdif]
                },
                {
                    "name": "LikeQuit",
                    "content": [tables.create_breakdown_cgstoplik]
                },
                {
                    "name": "Dependancy",
                    "content": [tables.create_breakdown_dcglongg_dcg7totg2_depend]
                },
                {
                    "name": "AttitudeQuitFut",
                    "content": [tables.create_breakdown_dgender_dcgtrystp]
                },
                {
                    "name": "StopSmokeMethods",
                    "content": [tables.create_breakdown_age1215_dcgoft_methodv2]
                },
                {
                    "name": "FamAware",
                    "content": [tables.create_breakdown_dcgstg3_dcgsec2]
                },
            ],
        },
        {
            "output_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_smokingcontext_source.xlsx",
            "table_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_smokingcontext_datatables_master.xlsx",
            "run_chapter": param.CHAPTER_SMOKING_CONTEXT,
            "chapter_number": "3",
            "sheets": [
                {
                    "name": "FriendsFamilySmoke",
                    "content": [tables.create_breakdown_age1115_dcgstg3_frfamsmoke]
                },
                {
                    "name": "FriendsFamilySmokev2",
                    "content": [tables.create_breakdown_age1115_dcgstg2_frfamsmoke]
                },
                {
                    "name": "SmokingStatus",
                    "content": [tables.create_breakdown_dfasbands_imdquin_dcgstg3]
                },
                {
                    "name": "FamilyAttitude",
                    "content": [tables.create_breakdown_dgender_age1315_dcgstg3_dcgfam]
                },
                {
                    "name": "FamilyAttitudev2",
                    "content": [tables.create_breakdown_dgender_age1315_dcgstg2_dcgfam]
                },
                {
                    "name": "FamilyAttCurrent",
                    "content": [tables.create_breakdown_dcgsec2_dcgfam]
                },
                {
                    "name": "ExposureSmoke",
                    "content": [tables.create_breakdown_age1115_dcgstg3_cgsmkexp]
                },
                {
                    "name": "ExposureSmokev2",
                    "content": [tables.create_breakdown_age1115_dcgstg2_cgsmkexp]
                },
                {
                    "name": "Attitudes",
                    "content": [tables.create_breakdown_dgender_age1115_dcgstg3_attitudes]
                },
                {
                    "name": "Attitudesv2",
                    "content": [tables.create_breakdown_dgender_age1115_dcgstg2_attitudes]
                },
            ],
        },
        {
            "output_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_ecigarette_source.xlsx",
            "table_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_ecigarette_datatables_master.xlsx",
            "run_chapter": param.CHAPTER_ECIGARETTE_USE,
            "chapter_number": "4",
            "sheets": [
                {
                    "name": "Aware",
                    "content": [tables.create_breakdown_dgender_age1315_cgelechd]
                },
                {
                    "name": "Source",
                    "content": [tables.create_breakdown_dgender_age1315_ecig_sources]
                },
                {
                    "name": "Status",
                    "content": [tables.create_breakdown_dgender_age1115_region_dcgstg5_dcgelec]
                },
                {
                    "name": "Attitudes",
                    "content": [tables.create_breakdown_dgender_age1115_ecig_attitudes]
                },
                {
                    "name": "RegLength",
                    "content": [tables.create_breakdown_dgender_cgellong]
                },
                {
                    "name": "RegSmoking",
                    "content": [tables.create_breakdown_dgender_cgnbavap]
                },
            ],
        },
        {
            "output_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_drugprev_source.xlsx",
            "table_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_drugprev_datatables_master.xlsx",
            "run_chapter": param.CHAPTER_DRUG_PREVALENCE,
            "chapter_number": "8",
            "sheets": [
                {
                    "name": "DrugUse",
                    "content": [tables.create_breakdown_dgender_age1115_region_ethnicgp5_druguse]
                },
                {
                    "name": "SummaryLastYr",
                    "content": [tables.create_breakdown_dgender_age1315_ddgyrty]
                },
                {
                    "name": "Occasions",
                    "content": [tables.create_breakdown_dgender_age1115_ddgoc]
                },
                {
                    "name": "DrugUseType",
                    "content": [tables.create_breakdown_dgender_age1115_drugusetype]
                },
                {
                    "name": "OccasionsPsych",
                    "content": [tables.create_breakdown_dgender_age1315_dgocleg]
                },
                {
                    "name": "OccasionslastYr",
                    "content": [tables.create_breakdown_age1315_ddgyrty5_ddgoc]
                },
                {
                    "name": "OccasionsAllDrug",
                    "content": [tables.create_breakdown_dgender_age1315_drugoccasion]
                },
                {
                    "name": "RecentPsych",
                    "content": [tables.create_breakdown_dgender_age1315_ddgtypleg]
                },
                {
                    "name": "OnceMonth",
                    "content": [tables.create_breakdown_dgender_age1215_ddgfq6]
                },
                {
                    "name": "UsualFreq",
                    "content": [tables.create_breakdown_dgender_age1215_ddgfq8]
                },
                {
                    "name": "UsualFreqLastYr",
                    "content": [tables.create_breakdown_dgender_age1315_ddgfq8_lastyr]
                },
                {
                    "name": "UsualFreqLastYrType",
                    "content": [tables.create_breakdown_ddgyrty5_ddgfq8_lastyr]
                },
                {
                    "name": "TruantExcClassA",
                    "content": [tables.create_breakdown_dtruexc_ddgyrcla]
                },
                {
                    "name": "TruantExcAny",
                    "content": [tables.create_breakdown_dtruexc_ddgfq6]
                },
                {
                    "name": "Offered",
                    "content": [tables.create_breakdown_dgender_age1115_drugoff]
                },
                {
                    "name": "Offered15Any",
                    "content": [tables.create_breakdown_dgender_age15_anydrugofftaken]
                },
                {
                    "name": "Aware",
                    "content": [tables.create_breakdown_age1115_drugaware]
                },
                {
                    "name": "Offered15Can",
                    "content": [tables.create_breakdown_dgender_age15_canofftaken]
                },
                {
                    "name": "Offered15ClassA",
                    "content": [tables.create_breakdown_dgender_age15_claofftaken]
                },
                {
                    "name": "AgeFirstDrug",
                    "content": [tables.create_breakdown_ddgageany11_ddgagexxx]
                },
                {
                    "name": "AgeFirstDrugSum",
                    "content": [tables.create_breakdown_ddgageany11_ddgfirst]
                },
                {
                    "name": "FirstDrugSum",
                    "content": [tables.create_breakdown_ddgageany11_ddgfttyp]
                },
                {
                    "name": "DrugRecent",
                    "content": [tables.create_breakdown_dgender_age1315_ddglttyp]
                },
            ],
        },
        {
            "output_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_youngwhodrugs_source.xlsx",
            "table_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_youngwhodrugs_datatables_master.xlsx",
            "run_chapter": param.CHAPTER_YOUNG_WHO_DRUGS,
            "chapter_number": "9",
            "sheets": [
                {
                    "name": "FromFirstTime",
                    "content": [tables.create_breakdown_dgender_ddgageany11_ddgfttyp_dgftwh]
                },
                {
                    "name": "FromMostRecent",
                    "content": [tables.create_breakdown_dgender_age1315_ddglttyp_dgltwh]
                },
                {
                    "name": "EaseObtain",
                    "content": [tables.create_breakdown_dgender_age_ddgofany_ddgget]
                },
                {
                    "name": "IntShop",
                    "content": [tables.create_breakdown_dgender_age1115_dgbuy]
                },
                {
                    "name": "IntShopLastYr",
                    "content": [tables.create_breakdown_ddgyrty5_dgbuy]
                },
                {
                    "name": "WhereObtain",
                    "content": [tables.create_breakdown_dgender_age1315_ddglttyp_dgltwhr]
                },
                {
                    "name": "WhoWith",
                    "content": [tables.create_breakdown_dgender_age1315_ddglttyp_whowith]
                },
            ],
        },
        {
            "output_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_drugcontext_source.xlsx",
            "table_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_drugcontext_datatables_master.xlsx",
            "run_chapter": param.CHAPTER_DRUG_CONTEXT,
            "chapter_number": "10",
            "sheets": [
                {
                    "name": "WhyFirst",
                    "content": [tables.create_breakdown_dgender_ddgageany11_ddgfttyp_ddgftwy]
                },
                {
                    "name": "WhyRecent",
                    "content": [tables.create_breakdown_dgender_age1315_ddglttyp_ddgoc_ddgltwy]
                },
                {
                    "name": "Attitudes",
                    "content": [tables.create_breakdown_dgender_age1115_drugattitudes]
                },
                {
                    "name": "FamAttitude",
                    "content": [tables.create_breakdown_dgender_age1115_ddgfam]
                },
                {
                    "name": "FamAttitudeKnow",
                    "content": [tables.create_breakdown_ddgfamknw_ddgfam]
                },
                {
                    "name": "Occasions",
                    "content": [tables.create_breakdown_ddgfam5_ddgoc]
                },
                {
                    "name": "LastTaken",
                    "content": [tables.create_breakdown_dfasbands_imdquin_ddglast3]
                 },
            ],
        },
        {
            "output_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_multibehaviour_source.xlsx",
            "table_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_multibehaviour_datatables_master.xlsx",
            "run_chapter": param.CHAPTER_MULTI_BEHAVIOURS,
            "chapter_number": "11",
            "sheets": [
                {
                    "name": "BehavioursEver",
                    "content": [tables.create_breakdown_age1115_behavevr]
                 },
                {
                    "name": "BehavioursRecent",
                    "content": [tables.create_breakdown_age1115_behavrec]
                 },
                {
                    "name": "Overlapping",
                    "content": [tables.create_breakdown_age1115_behavoverlap]
                 },
                {
                    "name": "Attitudes",
                    "content": [tables.create_breakdown_age1115_attitudes]
                 },
            ],
        },
        {
            "output_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_wellbeing_source.xlsx",
            "table_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_wellbeing_datatables_master.xlsx",
            "run_chapter": param.CHAPTER_WELLBEING,
            "chapter_number": "13",
            "sheets": [
                {
                    "name": "LifeSat",
                    "content": [tables.create_breakdown_dgender_age1115_region_dlifsat]
                 },
                {
                    "name": "LifeSatBehaviour",
                    "content": [tables.create_breakdown_cg7_dallast5_ddgmonany_dmulticount_dlifsat]
                 },
                {
                    "name": "LifeWorth",
                    "content": [tables.create_breakdown_dgender_age1115_region_dlifwor]
                 },
                {
                    "name": "LifeWorthBehaviour",
                    "content": [tables.create_breakdown_cg7_dallast5_ddgmonany_dmulticount_dlifwor]
                 },
                {
                    "name": "LifeHappy",
                    "content": [tables.create_breakdown_dgender_age1115_region_dlifhap]
                 },
                {
                    "name": "LifeHappyBehaviour",
                    "content": [tables.create_breakdown_cg7_dallast5_ddgmonany_dmulticount_dlifhap]
                 },
                {
                    "name": "LifeAnxious",
                    "content": [tables.create_breakdown_dgender_age1115_region_dlifanx]
                 },
                {
                    "name": "LifeAnxiousBehaviour",
                    "content": [tables.create_breakdown_cg7_dallast5_ddgmonany_dmulticount_dlifanx]
                 },
                {
                    "name": "LifeLow",
                    "content": [tables.create_breakdown_dgender_age1115_dliflow]
                 },
                {
                    "name": "LonelyComp",
                    "content": [tables.create_breakdown_dgender_age1115_region_dloncomp]
                 },
                {
                    "name": "LonelyCompBehaviour",
                    "content": [tables.create_breakdown_cg7_dallast5_ddgmonany_dmulticount_dloncomp]
                 },
                {
                    "name": "Lonely",
                    "content": [tables.create_breakdown_dgender_age1115_region_lonlonely]
                 },
                {
                    "name": "LonelyBehaviour",
                    "content": [tables.create_breakdown_cg7_dallast5_ddgmonany_dmulticount_lonlonely]
                 },
                {
                    "name": "LonelyTalkTo",
                    "content": [tables.create_breakdown_dgender_age1115_lontalk]
                 },
                {
                    "name": "LonelyLeftOut",
                    "content": [tables.create_breakdown_dgender_age1115_lonout]
                 },
                {
                    "name": "LonelyAlone",
                    "content": [tables.create_breakdown_dgender_age1115_lonalone]
                 },
            ],
        },
    ]

    return all_chapters


def get_ci_chapters():
    ci_chapters = [
        {
            "table_path": param.OUTPUT_DIR / "MasterFiles" / "sdd_ci_datatables_master.xlsx",
            "chapter_number": "ci",
            },
        ]

    return ci_chapters
