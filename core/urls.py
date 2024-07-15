
from django.urls import path
from .views import*



urlpatterns = [
    path('', Home,name="home"),
    path('user_registration', UserRegistration,name="user_registration"),
    path('instructor_registration', InstructorRegistration,name="instructor_registration"),
    path('add_education', AddEducation,name="add_education"),
    path('add_kyc_doc', AddKycDocument,name="add_kyc_doc"),
    path('user_login', UserLogin,name="user_login"),
    path('verify_otp', VerifyOtp,name="verify_otp"),
    path('log_out', LogOut,name="log_out"),
    path('course/<int:cid>', categoryWiseCourse,name="category_course"),
    path('detail_course/<int:id>', courseDetailView,name="detail_course"),
    path('detail_live_course/<int:id>', livecourseDetailView,name="detail_live_course"),
    path('play_course/<int:id>', playCourseView,name="play_course"),
    path('not_found', NotFoundView,name="not_found"),
    path('purchaseCourse', PurchaseCourse,name="purchaseCourse"),
    path('user_purchased_list', UserPurchasedCourse,name="user_purchased_list"),
    path('user_purchased_live_list', UserPurchasedliveCourse,name="user_purchased_live_list"),
    

    path('user_wish_list', UserWishlist,name="user_wish_list"),
    path('add_to_wishlist', AddToWishlist,name="add_to_wishlist"),
    path('remove_from_wishlist', RemoveFromWishlist,name="remove_from_wishlist"),
    path('get_user_details/<int:id>', GetUserDetails,name="get_user_details"),
    path('approveUser', ApproveUser,name="approveUser"),
    path('disapproveUser', DisapproveUser,name="disapproveUser"),
    path('deleteUser', DeleteUser,name="deleteUser"),
    path('user_dashboard', userDashboard,name="user_dashboard"),
    path('view_user_profile', viewUserProfile,name="view_user_profile"),
    path('uploadUserProfile', uploadUserProfile,name="uploadUserProfile"),
    path('teacher-revenue/', teacher_revenue, name='teacher_revenue'),
    
    path('cart', CartDetails, name='cart'),
    path('apply_cart_coupon/<int:id>', ApplyCartCoupon, name='apply_cart_coupon'),
    path('apply_course_coupon/<int:id>', ApplyCourseCoupon, name='apply_course_coupon'),
    path('remove_course_coupon/<int:id>', RemoveCourseCoupon, name='remove_course_coupon'),
    path('add_to_cart/<int:id>', addToCart, name='add_to_cart'),
    path('delete_from_cart/<int:id>', deleteFromCart, name='delete_from_cart'),
    path('remove_from_cart/<int:id>', removeFromCart, name='remove_from_cart'),
    path('cart_checkout', cartCheckout, name='cart_checkout'),
    path('admin/core/customuser/<str:pk>/change/', custom_user_change_view, name='customuser_customuser_change'),
    
    
    path('initEnrollPayment', initEnrollPayment, name='initEnrollPayment'),
    path('checkoutSubscription', checkoutSubscription, name='checkoutSubscription'),
    path('verifySignature', VerifySignature, name='verifySignature'),
    path('subcription', subscription, name='subscription'),
    path('callback', callback, name='callback'),
    path('subscribe', subscribe, name='subscribe'),
    path('certificate/<cid>', usercertificate, name='certificate'),
    path('support', support, name='support'),
    path('aboutus', aboutUs, name='aboutus'),
    path('contactus', ContactUs, name='contactus'),
    path('privacy_policy', Privacy_Policy, name='privacy_policy'),
    path('terms_conditions', TermsAndConditions, name='terms_conditions'),
    path('course_query', courseQuery, name='course_query'),
    path('new_category_request', NewCategoryRequest, name='new_category_request'),
    path('search', GlobalSearchView.as_view(), name='search'),
    path('filter_course', filterCourse, name='filter_course'),
    path('download_invoice/<int:id>', download_invoice_view,name='download_invoice'),

    #=========Notification related urls==========#
    path('remove_notification/<int:id>/', remove_notification, name='remove_notification'),
    path('notification/mark_all_read/', mark_all_read, name='mark_all_read'),
    path('notification/delete_all_read/', delete_all_read, name='delete_all_read'),
    path('notification/', notification_list, name='notification_list'),
    path('notification/<int:id>/', notification_view, name='notification_view'),
    path('notification_count/<int:id>/',user_notifications_count,name='notification_count'),

    path('api/course_query/', CourseQueryAPIView.as_view(), name='course_query_api'),
    path('api/get_user_queries/', GetUserQueriesAPIView.as_view(), name='get_user_queries_api'),
    path('update_topic_progress', updateTopicProgress, name='update_topic_progress'),
    
   
   
]
