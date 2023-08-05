# coding=utf-8
from __future__ import unicode_literals
from .. import Provider as PersonProvider


class Provider(PersonProvider):
    formats = (
        '{{first_name}} {{last_name}}',
        '{{first_name}} {{last_name}}',
        '{{last_name}}, {{first_name}}'
    )

    first_names = (
        'अभय','आदित्य','अजित','अखिल','अमर','आनन्द','अंकुर','अनुपम','अशोक','चन्दना','गणेश','गौतम','गोविंदा','हनुमान्','इन्द्रजित','ईश',
        'जगन्नाथ','जगदीश','जयदेव','जितेन्द्र','कैलाश','कालिदास','कम्बोज','किरण','ललित','मानदीप','मोहन','मुकेश','नरेन्द्र','नारायण','निखिल','प्रभाकर',
        'प्रबोध','प्रदीप','प्रणव','प्रेम','राजीव','रतन','रोहन','विष्णु','विक्रम','विजया','विजय','विवेक','यश',
        'अभिलाषा','अदिती','ऐश्वर्या','अमिता','अंकिता','आशा','अवनी','भरत','चेतना','दिव्या','एषा','इन्दु','जया','जयन्ती','ज्योत्सना','कान्ती','कुमारी',
        'लता','लीला','मालती','मोहिनी','निशा','पूर्णिमा','पुष्पा','रचना','रजनी','रश्मी','रिया','सरला','सरस्वती','सावित्री','शक्ति','शान्ता','शर्मिला','श्यामा',
        'सुलभा','तृष्णा','विद्या'
    )

    last_names = (
        'पाटिल','शर्मा','आचार्य','अग्रवाल','सिंह','अहलुवालिया','आहूजा','पुष्कर','शिरोळे','गायकवाड','गावित','शिरोळे','बापट','अरोड़ा','बाबू',
        'बादामी','जमानत','बजाज','बक्षी','बालकृष्णन','बालासुब्रमणियम','बसु','भंडारी','चौधरी','चौहान','छाबरा','दादा','डानी','डार', 'दारा', 'दत्ता',
        'दवे', 'दयाल', 'धालीवाल','दीक्षित', 'दोषी', 'दुआ', 'दूबे' ,'ढींगरा','वाल', 'साया', 'बना', 'ड़ाल' ,'गर्ग' ,'गणेश','गांगुली','गुप्ता',
        'हेगडे','जोशी','काले','कृष्णा', 'कृष्णमूर्ति', 'कृष्णन' ,'कुलकर्णी', 'कुमार', 'कुण्डा', 'नाम', 'रामलला', 'लता', 'लोदी', 'लोकनाट्यों',
        'विकावि', 'लाल', 'लाला' ,'वफादार', 'लूथरा' ,'मदन', 'मगर' ,'भारत', 'महावीर' , 'महादेव', 'महाजन', 'महाराज', 'मजूमदार', 'मल्लिक' ,'सेनाधीश',
        'माने' ,'मंगल', 'मंगत', 'रामशर्मा' ,'मणि', 'मान',  'श्रीविमल', 'कुमार', 'मंडल'
    )
