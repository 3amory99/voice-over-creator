from langdetect import detect



L = ["Geeksforgeeks is a computer science portal for geeks",
     "Geeksforgeeks - это компьютерный портал для гиков",
     "Geeksforgeeks es un portal informático para geeks",
     "Geeksforgeeks是面向极客的计算机科学门户",
     "Geeksforgeeks geeks के लिए एक कंप्यूटर विज्ञान पोर्टल है",
     "Geeksforgeeksは、ギーク向けのコンピューターサイエンスポータルです。",
     "يمكن أن يكون الكلام طريقة جيدة لدفع الرسوم المتحركة لتعبيرات الوجه. غالبًا ما تُستخدم البصمات لتمثيل الأوضاع الرئيسية في الكلام المرصود ، مثل موضع الشفتين والفك واللسان عند إنتاج صوت معين. يمكنك الاشتراك الان والاستمتاع بعروضنا المميزة، شكرا لكم"
     ]
for i in L:
    # Language Detection
    print(detect(i))

