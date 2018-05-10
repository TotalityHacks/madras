'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('django_admin_log', {
    'action_time': {
      type: DataTypes.DATE,
    },
    'object_id': {
      type: DataTypes.STRING,
    },
    'object_repr': {
      type: DataTypes.STRING,
    },
    'action_flag': {
      type: DataTypes.INTEGER,
    },
    'change_message': {
      type: DataTypes.STRING,
    },
  }, {
    tableName: 'django_admin_log',
    underscored: true,
    timestamps: false,
    schema: process.env.DATABASE_SCHEMA,
  });

  Model.associate = (models) => {
    Model.belongsTo(models.django_content_type, {
      foreignKey: 'content_type_id',
      
      as: '_content_type_id',
    });
    
    Model.belongsTo(models.registration_applicant, {
      foreignKey: 'user_id',
      
      as: '_user_id',
    });
    
  };

  return Model;
};

