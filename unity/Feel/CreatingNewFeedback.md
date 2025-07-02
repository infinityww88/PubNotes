创建新反馈非常简单。新建一个类，让它继承自MMF_Feedback，然后重写你需要的方法（通常是CustomInitialization、CustomPlayFeedback、CustomStopFeedback和CustomReset）。你可以参考其他反馈的实现方式，它们都有详细的注释。以下是一个可用作起点的模板

```C#
using UnityEngine;
using MoreMountains.Tools;

namespace MoreMountains.Feedbacks
{
    [AddComponentMenu("")]
    [FeedbackHelp("You can add a description for your feedback here.")]
    [FeedbackPath("ChosenPath/MyFeedbackNameGoesHere")]
    public class MMF_MyFeedbackName : MMF_Feedback
    {
        /// a static bool used to disable all feedbacks of this type at once
        public static bool FeedbackTypeAuthorized = true;
        /// use this override to specify the duration of your feedback (don't hesitate to look at other feedbacks for reference)
        public override float FeedbackDuration { get { return 0f; } }
        /// pick a color here for your feedback's inspector
    		#if UNITY_EDITOR
    			public override Color FeedbackColor { get { return MMFeedbacksInspectorColors.DebugColor; } }
    		#endif

    		protected override void CustomInitialization(MMF_Player owner)
    		{
    			base.CustomInitialization(owner);
    			// your init code goes here
    		}

        protected override void CustomPlayFeedback(Vector3 position, float feedbacksIntensity = 1.0f)
        {
            if (!Active || !FeedbackTypeAuthorized)
            {
                return;
            }            
            // your play code goes here
        }

        protected override void CustomStopFeedback(Vector3 position, float feedbacksIntensity = 1)
        {
	        if (!FeedbackTypeAuthorized)
	        {
		        return;
	        }            
	        // your stop code goes here
        }
    }
}
```

## Modifying an existing feedback

## The MMF_FeedbackBase class

## Extensions Repository

如果你创建了一个新的反馈效果，并认为它可能对其他人也有帮助；或者你正在寻找更多反馈效果或Feel工具，可以前往GitHub上的Feel扩展资源库查看。